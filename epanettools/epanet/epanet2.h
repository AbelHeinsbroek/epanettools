/*
**   EPANET2.H
**
** C/C++ header file for EPANET Programmers Toolkit
**
** Last updated on 2/14/08 (2.00.12)
*/

#ifndef EPANET2_H
#define EPANET2_H

// --- Define the EPANET toolkit constants

#define EN_ELEVATION    0    /* Node parameters */
#define EN_BASEDEMAND   1
#define EN_PATTERN      2
#define EN_EMITTER      3
#define EN_INITQUAL     4
#define EN_SOURCEQUAL   5
#define EN_SOURCEPAT    6
#define EN_SOURCETYPE   7
#define EN_TANKLEVEL    8
#define EN_DEMAND       9
#define EN_HEAD         10
#define EN_PRESSURE     11
#define EN_QUALITY      12
#define EN_SOURCEMASS   13
#define EN_INITVOLUME   14
#define EN_MIXMODEL     15
#define EN_MIXZONEVOL   16

#define EN_TANKDIAM     17
#define EN_MINVOLUME    18
#define EN_VOLCURVE     19
#define EN_MINLEVEL     20
#define EN_MAXLEVEL     21
#define EN_MIXFRACTION  22
#define EN_TANK_KBULK   23

#define EN_DIAMETER     0    /* Link parameters */
#define EN_LENGTH       1
#define EN_ROUGHNESS    2
#define EN_MINORLOSS    3
#define EN_INITSTATUS   4
#define EN_INITSETTING  5
#define EN_KBULK        6
#define EN_KWALL        7
#define EN_FLOW         8
#define EN_VELOCITY     9
#define EN_HEADLOSS     10
#define EN_STATUS       11
#define EN_SETTING      12
#define EN_ENERGY       13

#define EN_DURATION     0    /* Time parameters */
#define EN_HYDSTEP      1
#define EN_QUALSTEP     2
#define EN_PATTERNSTEP  3
#define EN_PATTERNSTART 4
#define EN_REPORTSTEP   5
#define EN_REPORTSTART  6
#define EN_RULESTEP     7
#define EN_STATISTIC    8
#define EN_PERIODS      9

#define EN_NODECOUNT    0    /* Component counts */
#define EN_TANKCOUNT    1
#define EN_LINKCOUNT    2
#define EN_PATCOUNT     3
#define EN_CURVECOUNT   4
#define EN_CONTROLCOUNT 5

#define EN_JUNCTION     0    /* Node types */
#define EN_RESERVOIR    1
#define EN_TANK         2

#define EN_CVPIPE       0    /* Link types */
#define EN_PIPE         1
#define EN_PUMP         2
#define EN_PRV          3
#define EN_PSV          4
#define EN_PBV          5
#define EN_FCV          6
#define EN_TCV          7
#define EN_GPV          8

#define EN_NONE         0    /* Quality analysis types */
#define EN_CHEM         1
#define EN_AGE          2
#define EN_TRACE        3

#define EN_CONCEN       0    /* Source quality types */
#define EN_MASS         1
#define EN_SETPOINT     2
#define EN_FLOWPACED    3

#define EN_CFS          0    /* Flow units types */
#define EN_GPM          1
#define EN_MGD          2
#define EN_IMGD         3
#define EN_AFD          4
#define EN_LPS          5
#define EN_LPM          6
#define EN_MLD          7
#define EN_CMH          8
#define EN_CMD          9

#define EN_TRIALS       0   /* Misc. options */
#define EN_ACCURACY     1
#define EN_TOLERANCE    2
#define EN_EMITEXPON    3
#define EN_DEMANDMULT   4

#define EN_LOWLEVEL     0   /* Control types */
#define EN_HILEVEL      1
#define EN_TIMER        2
#define EN_TIMEOFDAY    3

#define EN_AVERAGE      1   /* Time statistic types.    */
#define EN_MINIMUM      2 
#define EN_MAXIMUM      3
#define EN_RANGE        4

#define EN_MIX1         0   /* Tank mixing models */
#define EN_MIX2         1
#define EN_FIFO         2
#define EN_LIFO         3

#define EN_NOSAVE       0   /* Save-results-to-file flag */
#define EN_SAVE         1
#define EN_INITFLOW     10  /* Re-initialize flow flag   */



// --- define WINDOWS

#undef WINDOWS
#ifdef _WIN32
  #define WINDOWS
#endif
#ifdef __WIN32__
  #define WINDOWS
#endif

#undef WINDOWS
#undef __WIN32__

// --- define DLLEXPORT

#ifdef WINDOWS
  #ifdef __cplusplus
  #define DLLEXPORT extern "C" __declspec(dllexport) __stdcall
  #else
  #define DLLEXPORT __declspec(dllexport) __stdcall
  #endif
#else
  #ifdef __cplusplus
  #define DLLEXPORT extern "C"
  #else
  #define DLLEXPORT
  #endif
#endif


// --- declare the EPANET toolkit functions

extern int  ENepanet(char *, char *, char *, void (*) (char *));
extern int  ENopen(char *, char *, char * );
extern int  ENsaveinpfile(char * );
extern int  ENclose(void);

extern int  ENsolveH(void);
extern int  ENsaveH(void);
extern int  ENopenH(void);
extern int  ENinitH(int);
extern int  ENrunH(long * result );
extern int  ENnextH(long * result );
extern int  ENcloseH(void);
extern int  ENsavehydfile(char *  );
extern int  ENusehydfile(char *  );

extern int  ENsolveQ(void);
extern int  ENopenQ(void);
extern int  ENinitQ(int);
extern int  ENrunQ(long * result );
extern int  ENnextQ(long * result );
extern int  ENstepQ(long * result );
extern int  ENcloseQ(void);

extern int  ENwriteline(char *  );
extern int  ENreport(void);
extern int  ENresetreport(void);
extern int  ENsetreport(char *  );

extern int  ENgetcontrol(int, int * ci1, int * ci2, float * c1,
                      int * ci3, float * c2 );
extern int  ENgetcount(int, int * result);
extern int  ENgetoption(int, float * result );
extern int  ENgettimeparam(int, long * result );
extern int  ENgetflowunits(int * result );
extern int  ENgetpatternindex(char *, int * result );
extern int  ENgetpatternid(int, char * result );
extern int  ENgetpatternlen(int, int * result );
extern int  ENgetpatternvalue(int, int, float * result );
extern int  ENgetqualtype(int * result1, int * result );
extern int  ENgeterror(int, char * result, int);

extern int  ENgetnodeindex(char *, int * result );
extern int  ENgetnodeid(int, char * result );
extern int  ENgetnodetype(int, int * result );
extern int  ENgetnodevalue(int, int, float * result );

extern int  ENgetlinkindex(char *, int * result );
extern int  ENgetlinkid(int, char * result );
extern int  ENgetlinktype(int, int * result );
extern int  ENgetlinknodes(int, int  * result1, int * result2 );
extern int  ENgetlinkvalue(int, int, float * result );

extern int  ENgetversion(int * result );

extern int  ENsetcontrol(int, int, int, float, int, float);
extern int  ENsetnodevalue(int, int, float);
extern int  ENsetlinkvalue(int, int, float);
extern int  ENaddpattern(char *  );
extern int  ENsetpattern(int, float * floatarray, int nfloats);
extern int  ENsetpatternvalue(int, int, float);
extern int  ENsettimeparam(int, long);
extern int  ENsetoption(int, float);
extern int  ENsetstatusreport(int);
extern int  ENsetqualtype(int, char *, char *, char *  );


#endif
