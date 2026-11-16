# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Scenario time. A scenario writes absolute times around a reference time (ANCHOR, usually the task's key moment, e.g. the start of a
deployment window) and builds placeholders with T(). The container setup step shifts every placeholder by the same whole-hour amount
to match the real clock.
  After the shift, reference time = floor_hour(real now + lead minutes), so real now falls between lead minutes before and (60 - lead)
  minutes after the reference time.
  Shifting by whole hours only keeps written minutes (10:12 -> ?:12) and on-the-hour windows (14:00-15:00) on the hour; the weekday is
  computed from the shifted date.
Placeholders: "@@T<seconds relative to the reference>@@" (ISO 8601 UTC) or "@@T<seconds>|<strftime format>@@".
Weekday placeholder B(): "@@B<weekday seconds relative to the reference>@@" counts only weekday (UTC Mon-Fri) time between the reference time and that time.
  At run time it walks back the same amount of weekday time from the real reference time, so it never lands on a weekend and keeps its
  time of day and its order relative to other placeholders.
  A shift by the same amount would, when the run weekday differs from the reference weekday, move human records that were weekdays at
  build time (background chat, commits to shared documents) onto a weekend; use B() for those.
  Scenario-specific material whose calendar-date difference matters for grading (retention periods, expiry) keeps plain T(),
  because those date differences must not change.
"""
import datetime as _dt
import re

_PH = re.compile(r"@@T(-?\d+)(?:\|([^@]*))?@@")
_PHB = re.compile(r"@@B(-?\d+)(?:\+(\d+))?(?:\|([^@]*))?@@")
ISO = "%Y-%m-%dT%H:%M:%SZ"
_DAY = _dt.timedelta(days=1)
_WEEK_BIZ = 5 * 86400


def _parse(iso):
    return _dt.datetime.strptime(iso.replace("Z", ""), "%Y-%m-%dT%H:%M" + (":%S" if iso.count(":") == 2 else "")).replace(tzinfo=_dt.timezone.utc)


def _midnight(t):
    return t.replace(hour=0, minute=0, second=0, microsecond=0)


def _biz_between(a, b):
    """a <= b: weekday (UTC) seconds in [a, b)."""
    weeks = (b - a).days // 7
    total = weeks * _WEEK_BIZ
    t = a + _dt.timedelta(weeks=weeks)
    while t < b:
        nxt = min(b, _midnight(t) + _DAY)
        if t.weekday() < 5:
            total += int((nxt - t).total_seconds())
        t = nxt
    return total


def biz_shift(t, secs):
    """The time reached by moving t by secs seconds of weekday (UTC) time (negative = past). Weekends are skipped."""
    back = secs < 0
    rem = -secs if back else secs
    weeks = rem // _WEEK_BIZ                       # 7 days = 5 weekdays of time, whatever the span
    t = t - _dt.timedelta(weeks=weeks) if back else t + _dt.timedelta(weeks=weeks)
    rem -= weeks * _WEEK_BIZ
    while rem > 0:
        if back:
            start = _midnight(t - _dt.timedelta(microseconds=1))
            seg = int((t - start).total_seconds())
            if start.weekday() < 5:
                if rem < seg:
                    return t - _dt.timedelta(seconds=rem)
                rem -= seg
            t = start
            if rem == 0:            # weekday time ends exactly at a weekend boundary -> use the Friday 24:00 side (UTC Sat 00:00 = Friday afternoon US West)
                while (t - _dt.timedelta(microseconds=1)).weekday() >= 5:
                    t = _midnight(t - _dt.timedelta(microseconds=1))
                return t
        else:
            end = _midnight(t) + _DAY
            seg = int((end - t).total_seconds())
            if t.weekday() < 5:
                if rem <= seg:
                    return t + _dt.timedelta(seconds=rem)
                rem -= seg
            t = end
    return t


class Clock:
    def __init__(self, anchor, lead_minutes=20):
        self.anchor = _parse(anchor)
        self.lead = lead_minutes

    def T(self, iso, fmt=None):
        off = int((_parse(iso) - self.anchor).total_seconds())
        return f"@@T{off}|{fmt}@@" if fmt else f"@@T{off}@@"

    def B(self, iso, fmt=None):
        t = _parse(iso) if isinstance(iso, str) else iso
        # A time inside a UTC weekend (e.g. US West Friday afternoon = early UTC Saturday) or Monday 00:00 is written as
        # 'weekend boundary + seconds into the weekend'; when resolved it lands just after the boundary (within 86 s) in its original
        # order (see resolve_text).
        wk = None
        if t.weekday() >= 5 or (t.weekday() == 0 and t == _midnight(t)):
            sat = _midnight(t) - _dt.timedelta(days=(t.weekday() - 5) % 7)
            wk, t = int((t - sat).total_seconds()), sat
        off = -_biz_between(t, self.anchor) if t <= self.anchor else _biz_between(self.anchor, t)
        body = f"{off}+{wk}" if wk is not None else f"{off}"
        return f"@@B{body}|{fmt}@@" if fmt else f"@@B{body}@@"

    def seed(self):
        return {"lead_minutes": self.lead}


def offset_of(s):
    """For sorting: the seconds offset if s is a placeholder, else None. (Weekday placeholders hold weekday seconds; compare only within the same kind.)"""
    if not isinstance(s, str):
        return None
    m = _PH.fullmatch(s) or _PHB.fullmatch(s)
    return int(m.group(1)) if m else None


def shifted_anchor(now, lead_minutes):
    t = now + _dt.timedelta(minutes=lead_minutes)
    return t.replace(minute=0, second=0, microsecond=0)


def resolve_text(s, anchor_real):
    def sub(m):
        t = anchor_real + _dt.timedelta(seconds=int(m.group(1)))
        return t.strftime(m.group(2) or ISO)

    def subb(m):
        t = biz_shift(anchor_real, int(m.group(1)))
        if m.group(2):
            # A time inside a weekend is a zero-width point (the weekend boundary) in weekday time. If the run weekday differs, that point
            # becomes a midweek midnight, so adding the in-weekend seconds unchanged would put it after the following weekday records
            # and break the order -> scale down by 1/2000 (at most 86 s) so that only the relative order remains.
            t = t + _dt.timedelta(seconds=int(m.group(2)) // 2000)
        return t.strftime(m.group(3) or ISO)
    return _PHB.sub(subb, _PH.sub(sub, s))


def resolve(obj, anchor_real):
    if isinstance(obj, dict):
        return {resolve(k, anchor_real) if isinstance(k, str) else k: resolve(v, anchor_real) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve(v, anchor_real) for v in obj]
    if isinstance(obj, tuple):
        return tuple(resolve(v, anchor_real) for v in obj)
    if isinstance(obj, str):
        return resolve_text(obj, anchor_real)
    return obj
