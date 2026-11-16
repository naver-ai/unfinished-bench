/* Unfinished-Bench
 * Copyright (c) 2026-present NAVER Corp.
 * Apache-2.0
 */
/* Virtual clock: adds the relative FAKETIME offset (signed seconds) to the glibc 2.33+ file-time calls that
 * libfaketime 0.9.13 does not intercept (lstat64, fstat64, fstatat, fstatat64). stat, statx, lstat and fstat are left
 * to libfaketime so nothing is shifted twice. Load it before libfaketime. Does nothing if FAKETIME is not an integer. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "vc_conf.h"   /* environment variable, else the offset file */

static long off = 0;
static int ready = 0;

static void init(void) {
    if (ready) return;
    ready = 1;
    const char *e = vc_getenv("FAKETIME");
    if (!e) return;
    char *end;
    long v = strtol(e, &end, 10);
    if (end != e && *end == '\0') off = v;
}

static void shift(struct stat64 *b) {
    b->st_atim.tv_sec += off;
    b->st_mtim.tv_sec += off;
    b->st_ctim.tv_sec += off;
}

int lstat64(const char *p, struct stat64 *b) {
    static int (*real)(const char *, struct stat64 *);
    if (!real) real = dlsym(RTLD_NEXT, "lstat64");
    init();
    int r = real(p, b);
    if (r == 0 && off) shift(b);
    return r;
}

int fstat64(int fd, struct stat64 *b) {
    static int (*real)(int, struct stat64 *);
    if (!real) real = dlsym(RTLD_NEXT, "fstat64");
    init();
    int r = real(fd, b);
    if (r == 0 && off) shift(b);
    return r;
}

int fstatat64(int d, const char *p, struct stat64 *b, int f) {
    static int (*real)(int, const char *, struct stat64 *, int);
    if (!real) real = dlsym(RTLD_NEXT, "fstatat64");
    init();
    int r = real(d, p, b, f);
    if (r == 0 && off) shift(b);
    return r;
}

int fstatat(int d, const char *p, struct stat *b, int f) {
    static int (*real)(int, const char *, struct stat *, int);
    if (!real) real = dlsym(RTLD_NEXT, "fstatat");
    init();
    int r = real(d, p, b, f);
    if (r == 0 && off) shift((struct stat64 *)b);
    return r;
}

/* Virtual sleep: when the driver moves the scenario clock forward by a wait (the offset in the config file grows), a
 * sleeping process sleeps that much less, so a background script's `sleep 60` wakes after 60 seconds of scenario time.
 * Remaining = requested - (real time elapsed, CLOCK_MONOTONIC system call) - (offset increase), re-checked every 0.25 s.
 * Without the config file (server container, container tests) or for sleeps under 1 second, the original call runs. */
#include <time.h>
#include <errno.h>
#include <sys/syscall.h>

/* Sleep signal: a sleep of more than 1 second sends "<pid> <seconds>" on one datagram socket when it starts. The driver
 * moves the clock forward by that amount (inside the driver process) only while a command it classified as a wait is running,
 * and ignores the signal otherwise, so other sleeps (background work, for example) take real time. With no listener the
 * signal is silently dropped. No helper file or token is left in the container. */
#include <stdio.h>
#include <sys/socket.h>
#include <sys/un.h>
#define VC_SIG_PATH "/run/tzcompat.sock"
static void vc_notify(double d) {
    int e0 = errno;
    int s = socket(AF_UNIX, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (s >= 0) {
        struct sockaddr_un a;
        memset(&a, 0, sizeof a);
        a.sun_family = AF_UNIX;
        strncpy(a.sun_path, VC_SIG_PATH, sizeof a.sun_path - 1);
        char m[64];
        int n = snprintf(m, sizeof m, "%d %.3f\n", (int)getpid(), d);
        if (n > 0) (void)!sendto(s, m, (size_t)n, MSG_DONTWAIT | MSG_NOSIGNAL, (struct sockaddr *)&a, sizeof a);
        close(s);
    }
    errno = e0;
}

static long vc_file_off(int *ok) {
    int fd = open(VC_CONF_PATH, O_RDONLY | O_CLOEXEC);
    if (fd < 0) { *ok = 0; return 0; }
    char b[64];
    ssize_t k = read(fd, b, sizeof b - 1);
    close(fd);
    if (k <= 0) { *ok = 0; return 0; }
    b[k] = 0;
    *ok = 1;
    return strtol(b, NULL, 10);
}

static double vc_mono(void) {
    struct timespec t;
    syscall(SYS_clock_gettime, CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + t.tv_nsec / 1e9;
}

static int vc_vsleep(double d, int (*rns)(const struct timespec *, struct timespec *)) {
    int ok;
    long off0 = vc_file_off(&ok);
    double t0 = vc_mono();
    vc_notify(d);          /* signal after reading the starting offset */
    for (;;) {
        long o = vc_file_off(&ok);
        double rem = d - (vc_mono() - t0) - (ok ? (double)(o - off0) : 0.0);
        if (rem <= 0) return 0;
        double c = rem < 0.25 ? rem : 0.25;
        struct timespec ts;
        ts.tv_sec = (time_t)c;
        ts.tv_nsec = (long)((c - (double)ts.tv_sec) * 1e9);
        if (rns(&ts, NULL) != 0 && errno == EINTR) return -1;
    }
}

int nanosleep(const struct timespec *req, struct timespec *rem) {
    static int (*real)(const struct timespec *, struct timespec *);
    if (!real) real = dlsym(RTLD_NEXT, "nanosleep");
    int ok;
    vc_file_off(&ok);
    double d = req ? (double)req->tv_sec + req->tv_nsec / 1e9 : 0.0;
    if (!ok || d < 1.0) return real(req, rem);
    int r = vc_vsleep(d, real);
    if (r == 0 && rem) { rem->tv_sec = 0; rem->tv_nsec = 0; }
    return r;
}

int clock_nanosleep(clockid_t clk, int flags, const struct timespec *req, struct timespec *rem) {
    static int (*real)(clockid_t, int, const struct timespec *, struct timespec *);
    static int (*rns)(const struct timespec *, struct timespec *);
    if (!real) real = dlsym(RTLD_NEXT, "clock_nanosleep");
    if (!rns) rns = dlsym(RTLD_NEXT, "nanosleep");
    int ok;
    vc_file_off(&ok);
    if (!ok || !req || (clk != CLOCK_MONOTONIC && clk != CLOCK_REALTIME)) return real(clk, flags, req, rem);
    double d = (double)req->tv_sec + req->tv_nsec / 1e9;
    if (flags & TIMER_ABSTIME) {
        if (clk != CLOCK_MONOTONIC) return real(clk, flags, req, rem);
        d -= vc_mono();
    }
    if (d < 1.0) return real(clk, flags, req, rem);
    if (vc_vsleep(d, rns) != 0) return errno ? errno : EINTR;
    if (rem && !(flags & TIMER_ABSTIME)) { rem->tv_sec = 0; rem->tv_nsec = 0; }
    return 0;
}
