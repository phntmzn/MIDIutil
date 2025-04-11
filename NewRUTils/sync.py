import struct
import ctypes
from ctypes import POINTER, Structure, c_void_p, c_uint, c_ulong, c_ushort, c_int, c_char_p


#-----------------------------------------------------------------------------
# Function Prototype used in this dylib module
#-----------------------------------------------------------------------------


def InsertInSysexBuffer(lpMidiOut, thisEvent):
    # Simulate inserting a SysEx event into the buffer
    pass

def TrackMidiOut(lpMidiOut, dwMsg):
    # Simulate tracking MIDI output messages
    pass

def TurnNotesOff(lpMidiOut):
    # Simulate turning off all currently playing notes
    pass


#-----------------------------------------------------------------------------
# Open sync
# Enables sync for playback abd record for the sync mode selected
# to change the sync mod a previouslt opened sync device, open the 
# device again, passing the old hsync handle. reopening can be used
# to change hwnd, mode and/or wtimerperiod. any previous sync input
# setting is preserved

# on reopen the mode and/or wtimerperiod parameters can be set to
# USE_CURRENT to preserve previous settings
# 
# hSync is the handle to the already opened sync device if reopening in order
#to change settings, or zero if initially opening a device

#hWnd is the handle to the window that will recieve the sync messages
# MIDI_BEAT is sent on every beat the current tempo
#OUTBUFFER_READY is sent on every beat at the current tempo
#  25% full and is ready for more data

#mode can be set to:
# S_INT 
# S_MIDI

# wTimerPeriod is the requested timer period mS. The final actual
#capailities of the installed windows timer driver

#the function returns a handle to the sunc device if sync was correctly opened
#or an error value (less than MXMIDIERR_MAXERR) if there was an error opening
#-----------------------------------------------------------------------------

# Define constants
MXMIDIERR_MAXERR = -1
USE_CURRENT = -1
MMSYSERR_ALLOCATED = 4

# Define structures
class TIMECAPS(Structure):
    _fields_ = [("wPeriodMin", c_uint),
                ("wPeriodMax", c_uint)]

class SyncStruct(Structure):
    _fields_ = [("hWnd", c_void_p),
                ("wSyncMode", c_ushort),
                ("wFlags", c_ushort),
                ("nSysexBuffsActive", c_uint),
                ("wTimerPeriod", c_ushort),
                ("wTimerID", c_uint),
                ("lpMidiOutList", POINTER(c_void_p))]

# Define helper functions
def timeGetDevCaps(timeCaps, size):
    # Simulate getting timer capabilities
    timeCaps.wPeriodMin = 1
    timeCaps.wPeriodMax = 1000
    return 0

def timeBeginPeriod(period):
    # Simulate starting a timer period
    return 0

def timeEndPeriod(period):
    # Simulate ending a timer period
    pass

def timeSetEvent(period, resolution, callback, user, flags):
    # Simulate setting a timer event
    return 1

def timeKillEvent(timer_id):
    # Simulate killing a timer event
    pass

def SetResolution16(hSync, resolution):
    # Simulate setting resolution
    pass

def SetTempo16(hSync, tempo):
    # Simulate setting tempo
    pass

def FreeGlobalMem16(lpSY):
    # Simulate freeing global memory
    pass

# Python implementation of OpenSync16
def OpenSync16(hSync, hWnd, mode, wTimerPeriod):
    timeCaps = TIMECAPS()
    lpSY = None

    # Check if already open
    if hSync > MXMIDIERR_MAXERR and hSync is not None:
        lpSY = hSync

        # If timer was active, kill the timer
        if lpSY.wTimerID:
            timeKillEvent(lpSY.wTimerID)
            timeEndPeriod(lpSY.wTimerPeriod)
    else:
        # Allocate memory for the sync structure
        lpSY = SyncStruct()
        lpSY.lpMidiOutList = POINTER(c_void_p)()

    # Set the handle to the window that receives messages
    lpSY.hWnd = hWnd

    # Set the new sync mode
    if mode != USE_CURRENT:
        lpSY.wSyncMode = mode

    # Sync starts out disabled
    lpSY.wFlags = 0
    lpSY.nSysexBuffsActive = 0

    # Setup timer settings
    if wTimerPeriod != USE_CURRENT:
        lpSY.wTimerPeriod = wTimerPeriod

    lpSY.wTimerID = None

    # Set default resolution and tempo for MIDI playback
    SetResolution16(lpSY, 480)  # 480 ticks per beat
    SetTempo16(lpSY, 500000)   # 120 bpm

    # Enable the timer
    if timeGetDevCaps(timeCaps, ctypes.sizeof(timeCaps)) != 0:
        FreeGlobalMem16(lpSY)
        return MMSYSERR_ALLOCATED

    # Set the timer to the desired period
    if timeCaps.wPeriodMin <= lpSY.wTimerPeriod:
        lpSY.wTimerPeriod = lpSY.wTimerPeriod
    else:
        lpSY.wTimerPeriod = timeCaps.wPeriodMin

    if timeBeginPeriod(lpSY.wTimerPeriod) != 0:
        FreeGlobalMem16(lpSY)
        return MMSYSERR_ALLOCATED

    # Start the timer
    lpSY.wTimerID = timeSetEvent(lpSY.wTimerPeriod, lpSY.wTimerPeriod, None, lpSY, 0)
    if lpSY.wTimerID is None:
        FreeGlobalMem16(lpSY)
        return MMSYSERR_ALLOCATED

    return lpSY



#-----------------------------------------------------------------------------
#closeSync

#closes the sunc device and frees the sync structure
#returns 0 if successful, non-zero on error
#-----------------------------------------------------------------------------

def CloseSync16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return 0

    lpSync = hSync

    # Was internal sync enabled?
    if lpSync.wTimerID is not None:
        # Stop the timer
        timeKillEvent(lpSync.wTimerID)

        # Release the timer
        timeEndPeriod(lpSync.wTimerPeriod)

    # Disconnect all attached MIDI out devices from this sync device
    lpMOL = lpSync.lpMidiOutList
    while lpMOL and lpMOL.contents:
        lpMOL.contents.lpSync = None
        lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))

    # Free the lpMidiOutList structure
    FreeGlobalMem16(lpSync.lpMidiOutList)

    # Free the Sync structure
    FreeGlobalMem16(lpSync)

    return 1





#-----------------------------------------------------------------------------
#stopSync

#Disables the sunc device, but does not remove the time, if enabled.
#in contrast to the printed does not flush
# the output buffer
#---------------------------------------------------------------------------

def StopSync16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return

    lpSync = hSync

    # Disable the timer
    lpSync.wFlags = 0

    # Reset MIDI out for each output
    lpMOL = lpSync.lpMidiOutList
    while lpMOL and lpMOL.contents:
        lpMO = lpMOL.contents

        # Send MIDI stop if not in MIDI clock sync mode
        if lpSync.wSyncMode != "S_MIDI":  # Assuming "S_MIDI" is defined elsewhere
            if lpMO.dwFlags & "SYNC_OUTPUT":  # Assuming "SYNC_OUTPUT" is defined elsewhere
                midiOutShortMsg(lpMO.hMidiOut, 0xFC)  # 0xFC is MIDI_STOP

        # Reset the output
        ResetMidiOut16(lpMO)
        lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))


#-----------------------------------------------------------------------------
#PauseSync

# Diables the sunc device, but does not remove the timer, if enabled.
# This function does not flush the midi output buffers. If reset is TRUE
#  then MidioutReset is called, turning off any currently playing notes
# flushing the sysex buffers. If reset is FALSE then MidiOutReset is
# not called. Pausing sync without restting Midi out is intended for
# short duration pauses, since "stuck notes" may result from prolonged
# pauses without restting the outputs.
#-----------------------------------------------------------------------------
def PauseSync16(hSync, reset):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return

    lpSync = hSync

    # Save the state of the SYNC_RUNNING flag for later
    RUNNING_STATUS = 0x01  # Assuming RUNNING_STATUS is defined as 0x01
    SYNC_RUNNING = 0x02   # Assuming SYNC_RUNNING is defined as 0x02
    SYNC_ENABLED = 0x04   # Assuming SYNC_ENABLED is defined as 0x04

    lpSync.wFlags &= ~RUNNING_STATUS
    lpSync.wFlags |= (RUNNING_STATUS if (lpSync.wFlags & SYNC_RUNNING) else 0)

    # Disable the timer
    lpSync.wFlags &= ~SYNC_RUNNING
    lpSync.wFlags &= ~SYNC_ENABLED

    # If the reset parameter is True, reset MIDI out for each output
    if reset:
        lpMOL = lpSync.lpMidiOutList
        while lpMOL and lpMOL.contents:
            lpMO = lpMOL.contents

            # Send MIDI stop if not in MIDI clock sync mode
            if lpSync.wSyncMode != "S_MIDI":  # Assuming "S_MIDI" is defined elsewhere
                SYNC_OUTPUT = 0x08  # Assuming SYNC_OUTPUT is defined as 0x08
                if lpMO.dwFlags & SYNC_OUTPUT:
                    midiOutShortMsg(lpMO.hMidiOut, 0xFC)  # 0xFC is MIDI_STOP

            # Turn off any currently playing notes
            TurnNotesOff(lpMO)

            # Move to the next MIDI output
            lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))
#-----------------------------------------------------------------------------
# StartSync
# Enables the sync device and clears the ticks count

#---------------------------------------------------------------------
def StartSync16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return

    lpSync = hSync

    # Reset sync
    lpSync.dwFticks = 0
    lpSync.dwTicks = 0
    lpSync.nTicksSinceClock = 0
    lpSync.nTicksSinceBeat = 0
    lpSync.wTempoTicks = 0
    lpSync.dwLastTicks = 0
    lpSync.msPosition = 0

    # Clear the time of the last event
    lpMOL = lpSync.lpMidiOutList
    while lpMOL and lpMOL.contents:
        lpMO = lpMOL.contents
        lpMO.dwLastEventTicks = 0
        lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))

    # Restart sync
    ReStartSync16(hSync)
#-----------------------------------------------------------------------------
# restartSync
# Enables the sync device and clears the ticks count
#-----------------------------------------------------------------------
def ReStartSync16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return

    lpSync = hSync

    # Enable the timer
    SYNC_ENABLED = 0x04  # Assuming SYNC_ENABLED is defined as 0x04
    lpSync.wFlags |= SYNC_ENABLED

    # Allow a sync_done to be sent
    SENT_SYNCDONE = 0x08  # Assuming SENT_SYNCDONE is defined as 0x08
    lpSync.wFlags &= ~SENT_SYNCDONE

    # If it's not S_MIDI sync...
    if lpSync.wSyncMode != "S_MIDI":  # Assuming "S_MIDI" is defined elsewhere
        # Start the timer running (if S_MIDI, it will be started by reception of MIDI_START message)
        SYNC_RUNNING = 0x02  # Assuming SYNC_RUNNING is defined as 0x02
        lpSync.wFlags |= SYNC_RUNNING

        # Send start if not MIDI sync
        lpMOL = lpSync.lpMidiOutList
        while lpMOL and lpMOL.contents:
            lpMO = lpMOL.contents
            SYNC_OUTPUT = 0x08  # Assuming SYNC_OUTPUT is defined as 0x08
            if lpMO.dwFlags & SYNC_OUTPUT:
                midiOutShortMsg(lpMO.hMidiOut, 0xFA)  # 0xFA is MIDI_START

            # Move to the next MIDI output
            lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))
    else:
        # Restore the status of the SYNC_RUNNING flag for the S_MIDI sync mode
        RUNNING_STATUS = 0x01  # Assuming RUNNING_STATUS is defined as 0x01
        if lpSync.wFlags & RUNNING_STATUS:
            lpSync.wFlags &= ~RUNNING_STATUS
            lpSync.wFlags |= SYNC_RUNNING
#-----------------------------------------------------------------------------
# setTempo
# sets the current tempo. This function may be called at
# any time to change the tempo. the tempo is set microseconds
# seconds per midi beat so that tempo may be set fractionally

# returns 0 if successful, TIMERR_CANDO if the uSPerBeat parameter is
# zero.

#-----------------------------------------------------------------------------

def SetTempo16(hSync, uSPerBeat):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return "MXMIDIERR_BADHANDLE"

    # Tempo must be greater than zero
    if uSPerBeat == 0:
        return "MXMIDIERR_BADTEMPO"

    lpSync = hSync

    # Set the tempo
    SCALE = 1  # Assuming SCALE is defined as 1
    lpSync.dwTempo = uSPerBeat * SCALE

    # Test for uninitialized lpSyncIn -- without a sync input device
    # there is no valid destination for (sync) tempo changes
    if (lpSync.wFlags & 0x02) and (lpSync.lpSyncIn is not None):  # Assuming SYNC_RUNNING is 0x02
        lpMidiIn = lpSync.lpSyncIn

        # Calculate the elapsed ticks
        dwTicks = lpSync.dwTicks - lpMidiIn.dwLastEventTicks
        lpMidiIn.dwLastEventTicks = lpSync.dwTicks

        # Get a pointer to the buffer
        Qptr = ctypes.cast(
            ctypes.addressof(lpMidiIn.lpMidiInDataHead.contents) + lpMidiIn.pMidiInDataIn * ctypes.sizeof(lpMidiIn.lpMidiInDataHead.contents),
            ctypes.POINTER(ctypes.c_void_p)
        )

        # Store the data in the buffer
        Qptr.contents.time = dwTicks
        Qptr.contents.status = 0
        Qptr.contents.data1 = (uSPerBeat >> 16) & 0xFF
        Qptr.contents.data2 = (uSPerBeat >> 8) & 0xFF
        Qptr.contents.data3 = uSPerBeat & 0xFF

        # If necessary, wrap the pointer
        lpMidiIn.pMidiInDataIn += 1
        if lpMidiIn.pMidiInDataIn == lpMidiIn.nMidiInSize:
            lpMidiIn.pMidiInDataIn = 0

        # Send a message to the application
        PostMessage(lpMidiIn.hWnd, "MIDI_DATA", 0, ctypes.cast(lpMidiIn, ctypes.c_void_p))

    return 0


#-----------------------------------------------------------------------------
# setResolution

# Sets the resolution in ticks per midi beat. Higher values
# of resolution provide greater timing accuracy. This function should
# be called after the device is opended and before playback or record
# start.
#------------------------------------------------------------------
def SetResolution16(hSync, resolution):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return

    MAX_RESOLUTION = 960  # Assuming MAX_RESOLUTION is defined as 960
    if resolution > MAX_RESOLUTION:
        return

    lpSync = hSync

    # Set the resolution and calculate derived values
    lpSync.wResolution = resolution
    lpSync.nTicksPerClock = resolution // 24
    lpSync.dwTRtime = resolution * lpSync.wTimerPeriod * 256000

#-----------------------------------------------------------------------------
# GetTempo
#
# Gets the current tempo.  The tempo is set in microseconds
# per midi beat so that tempo may be set fractionally.
#-----------------------------------------------------------------------------
def GetTempo16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return 0
    else:
        SCALE = 1  # Assuming SCALE is defined as 1
        return hSync.dwTempo // SCALE

#-----------------------------------------------------------------------------
# GetResolution
#
# Gets the resolution in ticks per midi beat.  Higher values
# of resolution provide greater timing accuracy.
#-----------------------------------------------------------------------------
def GetResolution16(hSync):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return 0
    else:
        return hSync.wResolution
#-----------------------------------------------------------------------------
#  GetPosition
#
#  Returns the current playback position in either milliseconds since the
#  last time StartSync() was called (by specifying POS_MS for units) or in
#  elapsed ticks since the last time StartSync() was called (by specifying
#  POS_TICKS for units).
#-----------------------------------------------------------------------------
def GetPosition16(hSync, units):
    # If not open, ignore request
    if hSync is None or hSync <= MXMIDIERR_MAXERR:
        return 0

    lpSync = hSync

    # Determine the return value based on the requested units
    if units == "POS_MS":  # Assuming POS_MS is defined elsewhere
        rc = lpSync.msPosition
    elif units == "POS_TICKS":  # Assuming POS_TICKS is defined elsewhere
        rc = lpSync.dwTicks
    else:
        rc = 0

    return rc


#-----------------------------------------------------------------------------
# sync handler
#
# This function calculates the number of ticks since last message sent,
# based on the current sync mode.  If it is time, it sends the next midi
# message.
#
#   The algorithm used for timing is outlined below:
#
# given:
#   resolution in ticks/beat, tempo in uS/beat, and thistime in
#      nS/interrupt
# and
#   time in nS, corresponding to accumulated fractions of a tick
#
# then,
#   nticks = ((resolution * time) + (resolution * thistime)) / tempo
# and,
#   fticks = (thistime * resolution) - (nticks * tempo)
#
# since:
#   (resolution * thistime) is known in advance it is calculated
#   outside of this routine and stored in lpSync->dwTRtime.  It need
#   only be changed if the sync mode or resolution are changed.
#
# therefore:
#  nticks = (fticks + trtime)/tempo
#   fticks += trtime - nticks*tempo
#   elasped ticks += nticks
#-----------------------------------------------------------------------------
def sync(lpSync):
    # If sync is not running, return
    if (lpSync.wFlags & 0x02) != 0x02:  # Assuming SYNC_RUNNING is 0x02
        return

    lpSync.wFlags |= 0x10  # Assuming IN_SYNC is 0x10

    # Add time to the position accumulator for millisecond position
    lpSync.msPosition += lpSync.wTimerPeriod

    # Handle MIDI clock sync mode
    if lpSync.wSyncMode == "S_MIDI":  # Assuming "S_MIDI" is defined elsewhere
        if lpSync.wFlags & 0x20:  # Assuming MC_HOLD is 0x20
            nticks = (lpSync.dwFticks + lpSync.dwTRtime) // lpSync.dwTempo
            lpSync.dwFticks += lpSync.dwTRtime - (nticks * lpSync.dwTempo)
            lpSync.wTempoTicks += nticks
            lpSync.wFlags &= ~0x10  # Clear IN_SYNC
            return

        if lpSync.wFlags & 0x40:  # Assuming MC_RESYNC is 0x40
            lpSync.dwFticks = 0
            nticks = lpSync.nTicksPerClock - (lpSync.dwTicks - lpSync.dwLastTicks)
            lpSync.dwLastTicks = lpSync.dwTicks + nticks
            lpSync.wFlags &= ~0x40  # Clear MC_RESYNC
        else:
            nticks = (lpSync.dwFticks + lpSync.dwTRtime) // lpSync.dwTempo
            lpSync.dwFticks += lpSync.dwTRtime - (nticks * lpSync.dwTempo)
            lpSync.wTempoTicks += nticks

            if (lpSync.dwTicks - lpSync.dwLastTicks + nticks) >= lpSync.nTicksPerClock:
                nticks = lpSync.nTicksPerClock - 1 - (lpSync.dwTicks - lpSync.dwLastTicks)
                lpSync.wFlags |= 0x20  # Set MC_HOLD
    else:
        nticks = (lpSync.dwFticks + lpSync.dwTRtime) // lpSync.dwTempo
        lpSync.dwFticks += lpSync.dwTRtime - (nticks * lpSync.dwTempo)
        lpSync.nTicksSinceClock += nticks

    lpSync.dwTicks += nticks
    lpSync.nTicksSinceBeat += nticks

    if lpSync.nTicksSinceBeat >= lpSync.wResolution:
        PostMessage(lpSync.hWnd, "MIDI_BEAT", 0, ctypes.cast(lpSync, ctypes.c_void_p))
        lpSync.nTicksSinceBeat -= lpSync.wResolution

    nclocks = 0
    if lpSync.wSyncMode != "S_MIDI":
        while lpSync.nTicksSinceClock >= lpSync.nTicksPerClock:
            nclocks += 1
            lpSync.nTicksSinceClock -= lpSync.nTicksPerClock

    lpMOL = lpSync.lpMidiOutList
    fDone = True

    while lpMOL and lpMOL.contents:
        lpMO = lpMOL.contents

        nc = nclocks
        if (lpMO.dwFlags & 0x08) and (lpSync.wSyncMode != "S_MIDI"):  # Assuming SYNC_OUTPUT is 0x08
            while nc > 0:
                midiOutShortMsg(lpMO.hMidiOut, 0xF8)  # 0xF8 is MIDI_CLOCK
                nc -= 1

        thisEvent = ctypes.cast(
            ctypes.addressof(lpMO.lpMidiOutDataHead.contents) + lpMO.pMidiOutDataOut * ctypes.sizeof(lpMO.lpMidiOutDataHead.contents),
            ctypes.POINTER(ctypes.c_void_p)
        )

        if lpMO.wSpan != 0:
            fDone = False

            while (thisEvent.contents.time <= lpSync.dwTicks - lpMO.dwLastEventTicks) and \
                  (lpMO.wSpan != 0) and \
                  ((lpMO.dwFlags & 0x100 == 0) or (thisEvent.contents.status == 0xF0)):  # Assuming SENDING_SYSEX is 0x100 and SYSEX is 0xF0
                lpMO.dwLastEventTicks += thisEvent.contents.time

                if thisEvent.contents.status == 0:
                    newTempo = (thisEvent.contents.data2 << 8) + thisEvent.contents.data3
                    if newTempo != 0:
                        lpSync.dwTempo = newTempo
                else:
                    if thisEvent.contents.status == 0xF0:  # SYSEX
                        InsertInSysexBuffer(lpMO, thisEvent)
                    else:
                        dwMsg = thisEvent.contents.data1
                        midiOutShortMsg(lpMO.hMidiOut, dwMsg)
                        TrackMidiOut(lpMO, dwMsg)

                lpMO.pMidiOutDataOut += 1
                if lpMO.pMidiOutDataOut == lpMO.nMidiOutSize:
                    lpMO.pMidiOutDataOut = 0

                if lpMO.wSpan == (lpMO.nMidiOutSize >> 2):
                    PostMessage(lpMO.hWnd, "OUTBUFFER_READY", 0, ctypes.cast(lpMO, ctypes.c_void_p))

                lpMO.wSpan -= 1

                thisEvent = ctypes.cast(
                    ctypes.addressof(lpMO.lpMidiOutDataHead.contents) + lpMO.pMidiOutDataOut * ctypes.sizeof(lpMO.lpMidiOutDataHead.contents),
                    ctypes.POINTER(ctypes.c_void_p)
                )

        lpMOL = ctypes.cast(ctypes.addressof(lpMOL.contents) + ctypes.sizeof(c_void_p), POINTER(c_void_p))

    if fDone and (lpSync.nSysexBuffsActive == 0) and ((lpSync.wFlags & 0x08) == 0):  # Assuming SENT_SYNCDONE is 0x08
        PostMessage(lpSync.hWnd, "SYNC_DONE", 0, ctypes.cast(lpSync, ctypes.c_void_p))
        lpSync.wFlags |= 0x08  # Set SENT_SYNCDONE

    lpSync.wFlags &= ~0x10  # Clear IN_SYNC



#-----------------------------------------------------------------------------
# syncTimer callback function
#
# This callback processes the periodic timer events for internal sync
# and serves as a timebase for midi sync.
#
# Parameter dwUser is lpSync.  Other parameters are unused.
#-----------------------------------------------------------------------------
def syncTimer(wTimerID, wMsg, dwUser, dw1, dw2):
    # Don't call sync if already servicing a MIDI clock event
    lpSync = ctypes.cast(dwUser, ctypes.POINTER(SyncStruct)).contents
    IN_SYNC = 0x10  # Assuming IN_SYNC is defined as 0x10
    if (lpSync.wFlags & IN_SYNC) == 0:
        sync(lpSync)
#-----------------------------------------------------------------------------
# midi sync handler
#
# This function is called when the sync in device receives a midi clock
# message.  It calculates a new tempo based on the number of ticks since
# the last clock.
#-----------------------------------------------------------------------------
def MidiClock(lpSync):
    # Next sync() will be a re-sync
    MC_RESYNC = 0x40  # Assuming MC_RESYNC is defined as 0x40
    lpSync.wFlags |= MC_RESYNC

    # We are no longer holding the count
    MC_HOLD = 0x20  # Assuming MC_HOLD is defined as 0x20
    lpSync.wFlags &= ~MC_HOLD

    # Generate these ticks
    sync(lpSync)

    # Calculate new tempo
    lpSync.dwTempo -= ((lpSync.nTicksPerClock - lpSync.wTempoTicks) *
                       (lpSync.dwTempo // lpSync.wResolution))

    # Clear tempo tick count
    lpSync.wTempoTicks = 0