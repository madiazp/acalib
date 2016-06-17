/*
*+
*  Name:
*     prm_par.h

*  Type of Module:
*     C include file.

*  Purpose:
*     Define public constants for the PRM system.

*  Description:
*     This file defines machine-dependent public constants for the
*     PRM system (used to be called PRIMDAT).

*  Machine-specific features used:
*     (platform x86_64-unknown-linux-gnu, Fortran compiler gfortran)
*     The machine DOES appear to have IEEE floats.
*     The machine is LITTLE-endian
*     The CPU DOES NOT throw SIGFPE on denormalized numbers.

*  Authors:
*     RFWS: R.F. Warren-Smith (STARLINK, RAL)
*     ./make-prm-par program

*  History:
*     9-AUG-1988 (RFWS):
*        Original version.
*     25-OCT-1991 (RFWS):
*        Adapted for SUN4 systems from the original VMS file.
*     11-Jan-2016 (./make-prm-par):
*        Generated
*     No further changes -- do not edit this file

*  Copyright:
*     Copyright 1988, 1991, 1992, 1995, 2004, 2005, CCLRC 2012 STFC

*-
*/


/* HDS data type codes. */
#define VAL__NAMB "_BYTE"
#define VAL__NAMUB "_UBYTE"
#define VAL__NAMW "_WORD"
#define VAL__NAMUW "_UWORD"
#define VAL__NAMI "_INTEGER"
#define VAL__NAMK "_INT64"
#define VAL__NAMR "_REAL"
#define VAL__NAMD "_DOUBLE"

/* Bad values, used for flagging undefined data. */
#define VAL__BADUB 255
#define VAL__BADB (-127 - 1)
#define VAL__BADUW 65535
#define VAL__BADW (-32767 - 1)
#define VAL__BADI (-2147483647 - 1)
#define VAL__BADK (-9223372036854775807LL - 1)
#define VAL__BADR -3.40282347e+38F
#define VAL__BADD -1.7976931348623157e+308

/* Machine precision. */
#define VAL__EPSUB 1
#define VAL__EPSB 1
#define VAL__EPSUW 1
#define VAL__EPSW 1
#define VAL__EPSI 1
#define VAL__EPSK 1LL
#define VAL__EPSR 1.19209290e-07F
#define VAL__EPSD 2.2204460492503131e-16

/* Maximum (most positive) non-bad value. */
#define VAL__MAXUB 254
#define VAL__MAXB 127
#define VAL__MAXUW 65534
#define VAL__MAXW 32767
#define VAL__MAXI 2147483647
#define VAL__MAXK 9223372036854775807LL
#define VAL__MAXR 3.40282347e+38F
#define VAL__MAXD 1.7976931348623157e+308

/* Maximum (most positive) number. */
#define NUM__MAXUB 255
#define NUM__MAXB 127
#define NUM__MAXUW 65535
#define NUM__MAXW 32767
#define NUM__MAXI 2147483647
#define NUM__MAXK 9223372036854775807LL
#define NUM__MAXR 3.40282347e+38F
#define NUM__MAXD 1.7976931348623157e+308

/* Minimum (most negative) non-bad value. */
#define VAL__MINUB 0
#define VAL__MINB (-127)
#define VAL__MINUW 0
#define VAL__MINW (-32767)
#define VAL__MINI (-2147483647)
#define VAL__MINK (-9223372036854775807LL)
#define VAL__MINR -3.40282326e+38F
#define VAL__MIND -1.7976931348623155e+308

/* Minimum (most negative) number. */
#define NUM__MINUB 0
#define NUM__MINB (-127 - 1)
#define NUM__MINUW 0
#define NUM__MINW (-32767 - 1)
#define NUM__MINI (-2147483647 - 1)
#define NUM__MINK (-9223372036854775807LL - 1)
#define NUM__MINR -3.40282347e+38F
#define NUM__MIND -1.7976931348623157e+308

/* Number of basic machine units (bytes) used by a value. */
#define VAL__NBUB 1
#define VAL__NBB 1
#define VAL__NBUW 2
#define VAL__NBW 2
#define VAL__NBI 4
#define VAL__NBK 8
#define VAL__NBR 4
#define VAL__NBD 8

/* Smallest positive value. */
#define VAL__SMLUB 1
#define VAL__SMLB 1
#define VAL__SMLUW 1
#define VAL__SMLW 1
#define VAL__SMLI 1
#define VAL__SMLK 1LL
#define VAL__SMLR 1.40129846e-45F
#define VAL__SMLD 4.9406564584124654e-324

/* Number of characters required to format value as decimal string. */
#define VAL__SZUB 3
#define VAL__SZB 4
#define VAL__SZUW 5
#define VAL__SZW 6
#define VAL__SZI 11
#define VAL__SZK 20
#define VAL__SZR 15
#define VAL__SZD 24
