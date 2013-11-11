/*
 * bdump -- Dump info from a brother knitting machine file
 *

Copyright 2009  Steve Conklin 
steve at conklinhouse dot com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

This file is for experimentation, and reflects whatever I was working on.
It may be helpful as a starting point, but probably isn't of general use.

Book says max save of "approximately 13,600 stitches"
This is about 1700 bytes
2048 - 1700 = 348


---

#
# Pattern Number
# Position of the selector
# Pattern position for the selector setting
# Pattern position and number of repeats for each motif for selector (2) settings
# Variation key settings
# Memo display information
# Row numbers and memo key information

# 200 needles
# Max of 998 rows when entering your own patterns (depends on number of stitches in a row??)
# 998 rows would take 0x1F3 bytes for memo info, and there's not room where I think it should be
# pattern position is Yellow or Green (left or right)
# up to 6 motifs - 


 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

// defines that are probably correct and will stay

// Sizes
#define NEEDLELEN 13 // 13 bytes for 200 bits

// Pattern variations
#define VAR_REV  0x01 // reverse
#define VAR_MH   0x02 // mirror horizontal
#define VAR_SH   0x08 // stretch horizontal
#define VAR_SV   0x10 // stretch vertical
#define VAR_IV   0x04 // invert horizontal
#define VAR_KHC  0x20 // KHC
#define VAR_KRC  0x40 // KRC
#define VAR_MB   0x80 // M button
/*
    if (bd.variations & VAR_REV)
	printf("REVERSE ");
    if (bd.variations & VAR_MH)
	printf("MIRROR_H ");
    if (bd.variations & VAR_SH)
	printf("STRETCH H ");
    if (bd.variations & VAR_SV)
	printf("STRETCH V ");
    if (bd.variations & VAR_IV)
	printf("INVERT V ");
    if (bd.variations & VAR_KHC)
	printf("KHC ");
    if (bd.variations & VAR_KRC)
	printf("KRC ");
    if (bd.variations & VAR_UNK)
	printf("UNKNOWN ");
*/
// Selector switch
#define SEL_ONE  0x10
#define SEL_TWO  0x20

static void hex_dump(void *data, int size)
{
    /* dumps size bytes of *data to stdout. Looks like:
     * [0000] 75 6E 6B 6E 6F 77 6E 20
     *                  30 FF 00 00 00 00 39 00 unknown 0.....9.
     * (in a single line of course)
     */

    unsigned char *p = data;
    unsigned char c;
    int n;
    int marked = 0;
    char bytestr[4] = {0};
    char addrstr[10] = {0};
    char hexstr[ 16*3 + 5] = {0};
    char charstr[16*1 + 5] = {0};
    for(n=1;n<=size;n++) {
        if (n%16 == 1) {
            /* store address for this line */
            snprintf(addrstr, sizeof(addrstr), "%.4x",
               ((unsigned int)p-(unsigned int)data) );
        }
            
        c = *p;
        if (isalnum(c) == 0) {
            c = '.';
        }


        /* store hex str (for left side) */
        snprintf(bytestr, sizeof(bytestr), "%02X ", *p);
        strncat(hexstr, bytestr, sizeof(hexstr)-strlen(hexstr)-1);

        /* store char str (for right side) */
        snprintf(bytestr, sizeof(bytestr), "%c", c);
        strncat(charstr, bytestr, sizeof(charstr)-strlen(charstr)-1);

        if(n%16 == 0) { 
            /* line completed */
	    printf("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
	    hexstr[0] = 0;
	    charstr[0] = 0;
        } else if(n%8 == 0) {
            /* half line: add whitespaces */
            strncat(hexstr, "  ", sizeof(hexstr)-strlen(hexstr)-1);
            strncat(charstr, " ", sizeof(charstr)-strlen(charstr)-1);
        }
        p++; /* next byte */
    }

    if (strlen(hexstr) > 0) {
        /* print rest of buffer if not empty */
        printf("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
    }
}

/*
 * TODO This needs to be reworked. These represent the
 * values for all 200 needles. There are two copies in the file,
 * probably for 'this row' and 'next row'.
 *
 * For both the needle values, patterns, and memo information,
 * the data is always stored from higher to lower addresses
 * in the file.
 */
void olddumpNeedles(unsigned short *pp) {
    unsigned short *pp1 = pp;
    unsigned short pb;
    int i, j;
    for (i=0; i<NEEDLELEN; i++) {
	pb = htons(*pp1);
	//printf("0x%04X\n", pb);
	for (j=15; j>=0; j--) {
	    if (pb & (1<<j))
		printf("*");
	    else
		printf(" ");
	}
	pp1++;
    }
    printf("\n");
}

void dumpNeedles(unsigned short *pp) {
    void *pat = pp;
    pat += NEEDLELEN;
/*
    unsigned short *pp1 = pp;
    unsigned short pb;
    int i, j;
    for (i=0; i<NEEDLELEN; i++) {
	pb = htons(*pp1);
	//printf("0x%04X\n", pb);
	for (j=15; j>=0; j--) {
	    if (pb & (1<<j))
		printf("*");
	    else
		printf(" ");
	}
	pp1++;
    }
*/
    printf("\n");
}
/*
void dumpPattern(void *pat, int stitches, int rows) {
    // TODO finish this - how are things padded for odd numbers of stitches?
    return;
}
*/

int main (int argc, char *argv[]) {

    FILE *fin;
    char *infile;

    // our struct - doesn't reflect file structure
    typedef struct {
	unsigned char pos;
	unsigned char right;
	unsigned char copies;
    } motifstr, *motifptr;

    // This 7 byte structure is the file format
    // for the information about each custom
    // pattern 901-999
    typedef struct {
	unsigned char status;
	unsigned char unk1;
	unsigned char rows_t:4;
	unsigned char rows_h:4;
	unsigned char stitches_h:4;
	unsigned char rows_o:4;
	unsigned char stitches_o:4;
	unsigned char stitches_t:4;
	unsigned char num_h:4;
	unsigned char unk:4;
	unsigned char num_o:4;
	unsigned char num_t:4;
    } pgminfo, *ppgminfo;

    struct {
	pgminfo pgms[99];
	unsigned char head[1073];
	unsigned short needles1[NEEDLELEN];
	unsigned char afterfirst1[13];
	unsigned char variations;
	unsigned char afterfirst2[8];
	unsigned short needles2[NEEDLELEN];
	unsigned char tail1[186];
	unsigned char selector[1];
	unsigned char selfiller;
	unsigned char motifdata[20];
    } bd;

    unsigned char selector;
    motifstr motif[6];
    int nummotifs;
    unsigned char selone_pos;
    unsigned char selone_right;

    // misc variables
    int readlen;
    int i;
    unsigned char cval, *cptr;
    unsigned long foolong;

 
    if (argc != 2) {
	printf("usage: %s filename\n", argv[0]);
	exit(-1);
    }

    infile = argv[1];
    
    if (!(fin=fopen(infile, "r"))) {
	printf("Unable to open file %s\n", argv[1]);
	exit(-1);
    }

    printf("length of struct is %d\n", sizeof(bd));

    readlen = fread(&bd, 1, sizeof(bd), fin);
    if (readlen != sizeof(bd)) {
	printf("Failed read, %d\n", readlen);
	exit(-1);
    }

    fclose(fin);

    printf("===== programs =====\n");
    //for(i=0;i<100;i++) {
    for(i=0;i<5;i++) {
	ppgminfo pptr = &bd.pgms[i];
	unsigned int ival;
	//if (pptr->status == 1) {
	if (1) {
	    printf("Position %d:\n", i);
	    ival = (pptr->num_h * 100) + (pptr->num_t * 10) + (pptr->num_o);
	    printf("Status   0x%02X (%d)\n", pptr->status, pptr->status);
	    printf("  Pgm Number: % 3d\n", ival);
	    printf("  Unk nibble: % 3d\n", pptr->unk);
	    printf("    unk1        0x%02X (%d)\n", pptr->unk1, pptr->unk1);
	    ival = (pptr->rows_h * 100) + (pptr->rows_t * 10) + (pptr->rows_o);
	    printf("    Rows:     % 3d\n", ival);
	    ival = (pptr->stitches_h * 100) + (pptr->stitches_t * 10) + (pptr->stitches_o);
	    printf("    Stitches: % 3d\n", ival);

	    printf("--------\n");
	}
    }

    printf("===== head =====\n");
    hex_dump(bd.head, sizeof(bd.head));

    printf("===== Needles1 =====\n");
    dumpNeedles(bd.needles1);

    printf("===== afterfirst1 =====\n");
    hex_dump(bd.afterfirst1, sizeof(bd.afterfirst1));

    printf("===== Variations =====\n");
    printf("variations = 0x%02X - ", bd.variations);
    if (bd.variations & VAR_REV)
	printf("REVERSE ");
    if (bd.variations & VAR_MH)
	printf("MIRROR_H ");
    if (bd.variations & VAR_SH)
	printf("STRETCH H ");
    if (bd.variations & VAR_SV)
	printf("STRETCH V ");
    if (bd.variations & VAR_IV)
	printf("INVERT V ");
    if (bd.variations & VAR_KHC)
	printf("KHC ");
    if (bd.variations & VAR_KRC)
	printf("KRC ");
    //if (bd.variations & VAR_UNK)
    //printf("UNKNOWN ");
    printf("\n");

    printf("===== afterfirst2 =====\n");
    hex_dump(bd.afterfirst2, sizeof(bd.afterfirst2));

    printf("===== Needles2 =====\n");
    dumpNeedles(bd.needles2);

    printf("===== tail1 =====\n");
    hex_dump(bd.tail1, sizeof(bd.tail1));

    printf("===== selector =====\n"); // 0x7EA
    //printf("Selector = 0x%02X | %d\n", *bd.selector, *bd.selector);
    cval = *bd.selector & 0xF0;
    selector = cval;
    if (cval == SEL_ONE) {
	printf("Selector One (all over pattern):\n");
    } else if (cval == SEL_TWO) {
	printf("Selector Two (motifs):\n");
    } else {
	printf("Unknown selector value of 0x%X found\n", cval);
    }

    printf("===== selector low nibble =====\n"); // 0x7EA
    printf("Selector low nibble = 0x%02X\n", *bd.selector & 0x0F);

    printf("===== selfiller = 0x%02X =====\n", bd.selfiller);

    // read the motifs
    // Motif data is three bytes for each motif, but it is not
    // byte aligned - it is off alignment by 4 bits.
    cptr = &bd.motifdata[0];
    cval = *cptr & 0xF0;
    printf("MSB at beggining of motif info = 0x%02X\n", cval);
    for(i=5; i>=0; i--) {
	// First byte, skip MSB
	cval = *cptr & 0x0F; // LSB
	//printf("cval (LSB) = 0x%02X\n", cval);
	if (cval & 8) {
	    motif[i].right = 1;
	    cval &= 0x07;
	} else {
	    motif[i].right = 0;
	}
	if (cval > 1)
	    printf("Unexpected value of %d for position hundreds, motif %d\n", cval, i);
	motif[i].pos = cval * 100;
	// Second byte
	cptr++;
	//cval = *cptr;
	//printf("cval       = 0x%02X\n", cval);
	cval = (*cptr>>4) & 0x0F; // MSB
	motif[i].pos += cval * 10;
	cval = *cptr & 0x0F; // LSB
	motif[i].pos += cval;
	// Third byte
	cptr++;
	//cval = *cptr;
	//printf("cval       = 0x%02X\n", cval);
	cval = (*cptr>>4) & 0x0F; // MSB
	motif[i].copies = cval * 100;
	cval = *cptr & 0x0F; // LSB
	motif[i].copies += cval * 10;
	// Fourth byte
	cptr++;
	cval = (*cptr>>4) & 0x0F; // MSB
	//printf("cval (MSB) = 0x%02X\n", cval);
	motif[i].copies += cval;
	// Leave pointer so we grab LSB next round
	//printf("--\n");
    }
    // now in the last three nibbles is the starting
    // location for the pattern for Selector One
    // First byte, skip MSB
    cval = *cptr & 0x0F; // LSB
    if (cval & 8) {
	selone_right = 1;
	cval &= 0x07;
    } else {
	selone_right = 0;
    }
    if (cval > 1)
	printf("Unexpected value of %d for selector One position hundreds\n", cval);
    selone_pos = cval * 100;
    // Second byte
    cptr++;
    cval = (*cptr>>4) & 0x0F; // MSB
    selone_pos += cval * 10;
    cval = *cptr & 0x0F; // LSB
    selone_pos += cval;

    // see how many are in use - the first zero for
    // number of copies is the end
    nummotifs = 6;
    for (i=0; i<=5; i++) {
	if (motif[i].copies == 0) {
	    nummotifs = i;
	    break;
	}
    }

    printf("========== Selector Two (motifs) ==========\n");
    printf("%d motifs are used\n", nummotifs);
    for (i=0; i<=5; i++) {
	printf("Motif %d: ", i+1);
	printf(" %3d Copies ", motif[i].copies);
	if (motif[i].right)
	    printf("starting at %3d Right ", motif[i].pos);
	else
	    printf("starting at %3d Left  ", motif[i].pos);
	if (i+1 > nummotifs)
	    printf(" (UNUSED)\n");
	else
	    printf("\n");

    }
    printf("========== Selector One (all over pattern) ==========\n");
    if (selone_right)
	printf("Selector One pattern start is position %3d Right\n", selone_pos);
    else
	printf("Selector One pattern start is position %3d Left\n", selone_pos);
}
