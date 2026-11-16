/* Unfinished-Bench
 * Copyright (c) 2026-present NAVER Corp.
 * Apache-2.0
 */
/* Only for building libfaketime (-include): replaces its getenv calls with vc_getenv.
 * Defines the same feature macros as the top of libfaketime.c first, so stat64 etc. stay visible. */
#define _GNU_SOURCE
#define _LARGEFILE64_SOURCE 1
#include "vc_conf.h"
#define getenv vc_getenv
