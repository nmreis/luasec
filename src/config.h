/*--------------------------------------------------------------------------
 * LuaSec 0.5
 * Copyright (C) 2006-2014 Bruno Silvestre
 *
 *--------------------------------------------------------------------------*/

#ifndef LSEC_CONFIG_H
#define LSEC_CONFIG_H

#if defined(_WIN32)
#define LSEC_API __declspec(dllexport) 
#else
#define LSEC_API extern
#endif

#endif
