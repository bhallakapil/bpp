#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "types.h"
#include "rmd160.h"
#include "bigdeal.h"
#include "mp.h"
#include "binomial.h"
#include "output.h"
#include "os.h"
#include "collect.h"

#define ENTROPY_TO_COLLECT	RMDsize*4/3	/* 33% extra safety/paranoia */

static progparams_t parameters;
static byte nr_bridge_deals[L];
FILE *flog = NULL;

#define goedel(bignum)  (mp96_cmp(bignum, nr_bridge_deals) < 0)

static byte *
RMDhash(byte *value, int length)
{
	dword         MDbuf[RMDdwords];
	dword	      X[16];
	static byte   hashcode[RMDbytes];
	unsigned int  i;
	int	      nbytes;

	MDinit(MDbuf);

	for (nbytes=length; nbytes>=64; nbytes-=64) {
		for (i=0; i<16; i++) {
			X[i] = BYTES_TO_DWORD(value);
			value += 4;
		}
		compress(MDbuf, X);
	}
		
	MDfinish(MDbuf, value, length, 0);

	for (i=0; i<RMDbytes; i+=4) {
		hashcode[i]   =  MDbuf[i>>2];
		hashcode[i+1] = (MDbuf[i>>2] >>  8);
		hashcode[i+2] = (MDbuf[i>>2] >> 16);
		hashcode[i+3] = (MDbuf[i>>2] >> 24);
	}

	return (byte *)hashcode;
}

static void
init_goedel(void)
{
	byte a[L], b[L];

	n_over_k(52,13,a);
	n_over_k(39,13,b);
	mp96_mul(a,a,b);
	n_over_k(26,13,b);
	mp96_mul(a,a,b);

	mp96_assign(nr_bridge_deals, a);
}

static struct {
	byte	seed_sequence[4];
	byte	seed_random[RMDbytes];
	byte	seed_owner[RMDbytes];
} seed;

int
bigdeal_generate (int nboards, int lowboard, char *filename, char *formats, char *owner)
{
	int i;
	byte *hashcode;
	unsigned long seqno;
	dl_num dnumber;

	parameters.pp_lowboard = lowboard;
	parameters.pp_highboard = lowboard + nboards - 1;
	parameters.pp_nboards = nboards;

	os_start();
	collect_start();

	/* In a library, we assume entropy is collected from the OS automatically */
	os_collect();

	binomial_start();
	init_goedel();

	/* Finish entropy collection */
	collect_finish(seed.seed_random);

	if (formats == NULL || formats[0] == 0) {
		formats = "pbn";
	}

	if (owner == NULL || owner[0] == 0) {
		owner = "Default Owner";
	}

	(void) output_specify_formats(formats, 1);
	output_createfiles(filename, &parameters);

	hashcode = RMDhash((byte *) owner, strlen(owner));
	memcpy(seed.seed_owner, hashcode, RMDbytes);

	seqno = 0;
	for(i = parameters.pp_lowboard; i <= parameters.pp_highboard; i++) { 
		do {
			seqno++;
			seed.seed_sequence[0] = seqno & 0xFF;
			seed.seed_sequence[1] = (seqno>>8) & 0xFF;
			seed.seed_sequence[2] = (seqno>>16) & 0xFF;
			seed.seed_sequence[3] = (seqno>>24) & 0xFF;
			hashcode = RMDhash((byte *) &seed, sizeof(seed));
			memcpy(dnumber.dn_num, hashcode, L);
		} while(!goedel(dnumber.dn_num));
		output_hand(i, &dnumber);
	}

	output_closefiles();
	os_finish();
	return 0;
}
