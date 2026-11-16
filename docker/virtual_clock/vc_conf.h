/* Unfinished-Bench
 * Copyright (c) 2026-present NAVER Corp.
 * Apache-2.0
 */
/* Virtual clock settings, shared by libfaketime (getenv replaced at build time via vc_ft_getenv.h) and vclock_stat.so.
 * A real environment variable wins; otherwise one line from VC_CONF_PATH (the offset in seconds, e.g. +7266).
 * The agent container runs with /etc/ld.so.preload and this file and no environment variables, so `env` in the
 * agent's shell shows nothing. bash exports its own getenv, which would answer the library's getenv calls from
 * shell variables, so we read environ directly. */
#ifndef VC_CONF_H
#define VC_CONF_H
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define VC_CONF_PATH "/etc/tzcompat.conf"
extern char **environ;
static char vc_ft_[64];
static int vc_state_ = 0;

static inline const char *vc_env_lookup(const char *name) {
    size_t n = strlen(name);
    for (char **e = environ; e && *e; e++)
        if (!strncmp(*e, name, n) && (*e)[n] == '=') return *e + n + 1;
    return NULL;
}

static inline void vc_load_(void) {
    if (vc_state_) return;
    vc_state_ = 1;
    int fd = open(VC_CONF_PATH, O_RDONLY | O_CLOEXEC);
    if (fd < 0) return;
    ssize_t k = read(fd, vc_ft_, sizeof vc_ft_ - 1);
    close(fd);
    if (k <= 0) { vc_ft_[0] = 0; return; }
    vc_ft_[k] = 0;
    for (ssize_t i = 0; i < k; i++)
        if (vc_ft_[i] == '\n' || vc_ft_[i] == '\r' || vc_ft_[i] == ' ') { vc_ft_[i] = 0; break; }
}

/* FAKETIME = the offset from the file; FAKE_UTIME and FAKETIME_DONT_FAKE_MONOTONIC = 1 (same as the environment-variable setup) */
static inline char *vc_getenv(const char *name) {
    const char *v = vc_env_lookup(name);
    if (v) return (char *)v;
    if (strncmp(name, "FAKE", 4) != 0) return NULL;
    vc_load_();
    if (!vc_ft_[0]) return NULL;
    if (!strcmp(name, "FAKETIME")) return vc_ft_;
    if (!strcmp(name, "FAKE_UTIME") || !strcmp(name, "FAKETIME_DONT_FAKE_MONOTONIC")) return (char *)"1";
    return NULL;
}
#endif
