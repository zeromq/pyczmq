from pyczmq._cffi import C, ffi

functions = \
'''
/*  =========================================================================
    zmsg - working with multipart messages

    -------------------------------------------------------------------------
    Copyright (c) 1991-2013 iMatix Corporation <www.imatix.com>
    Copyright other contributors as noted in the AUTHORS file.

    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the 
    Free Software Foundation; either version 3 of the License, or (at your 
    option) any later version.

    This software is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
    ITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General 
    Public License for more details.

    You should have received a copy of the GNU Lesser General Public License 
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    =========================================================================
*/

//  Opaque class structure
typedef struct _zmsg_t zmsg_t;

//  @interface
//  Create a new empty message object
 zmsg_t *
    zmsg_new (void);

//  Destroy a message object and all frames it contains
 void
    zmsg_destroy (zmsg_t **self_p);

//  Receive message from socket, returns zmsg_t object or NULL if the recv
//  was interrupted. Does a blocking recv, if you want to not block then use
//  the zloop class or zmq_poll to check for socket input before receiving.
 zmsg_t *
    zmsg_recv (void *socket);

//  Send message to socket, destroy after sending. If the message has no
//  frames, sends nothing but destroys the message anyhow. Safe to call
//  if zmsg is null.
 int
    zmsg_send (zmsg_t **self_p, void *socket);

//  Return size of message, i.e. number of frames (0 or more).
 size_t
    zmsg_size (zmsg_t *self);

//  Return total size of all frames in message.
 size_t
    zmsg_content_size (zmsg_t *self);

//  Push frame to the front of the message, i.e. before all other frames.
//  Message takes ownership of frame, will destroy it when message is sent.
//  Returns 0 on success, -1 on error.
 int
    zmsg_push (zmsg_t *self, zframe_t *frame);

//  Remove first frame from message, if any. Returns frame, or NULL. Caller
//  now owns frame and must destroy it when finished with it.
 zframe_t *
    zmsg_pop (zmsg_t *self);

//  Add frame to the end of the message, i.e. after all other frames.
//  Message takes ownership of frame, will destroy it when message is sent.
//  Returns 0 on success. Deprecates zmsg_add, which did not nullify the
//  caller's frame reference.
 int
    zmsg_append (zmsg_t *self, zframe_t **frame_p);

//  Add frame to the end of the message, i.e. after all other frames.
//  Message takes ownership of frame, will destroy it when message is sent.
//  Returns 0 on success.
//  DEPRECATED - will be removed for next stable release
 int
    zmsg_add (zmsg_t *self, zframe_t *frame);

//  Push block of memory to front of message, as a new frame.
//  Returns 0 on success, -1 on error.
 int
    zmsg_pushmem (zmsg_t *self, const void *src, size_t size);

//  Add block of memory to the end of the message, as a new frame.
//  Returns 0 on success, -1 on error.
 int
    zmsg_addmem (zmsg_t *self, const void *src, size_t size);
    
//  Push string as new frame to front of message.
//  Returns 0 on success, -1 on error.
 int
    zmsg_pushstr (zmsg_t *self, const char *format, ...);

//  Push string as new frame to end of message.
//  Returns 0 on success, -1 on error.
 int
    zmsg_addstr (zmsg_t *self, const char *format, ...);

//  Pop frame off front of message, return as fresh string. If there were
//  no more frames in the message, returns NULL.
 char *
    zmsg_popstr (zmsg_t *self);

//  Push frame plus empty frame to front of message, before first frame.
//  Message takes ownership of frame, will destroy it when message is sent.
 void
    zmsg_wrap (zmsg_t *self, zframe_t *frame);

//  Pop frame off front of message, caller now owns frame
//  If next frame is empty, pops and destroys that empty frame.
 zframe_t *
    zmsg_unwrap (zmsg_t *self);

//  Remove specified frame from list, if present. Does not destroy frame.
 void
    zmsg_remove (zmsg_t *self, zframe_t *frame);

//  Set cursor to first frame in message. Returns frame, or NULL, if the 
//  message is empty. Use this to navigate the frames as a list.
 zframe_t *
    zmsg_first (zmsg_t *self);

//  Return the next frame. If there are no more frames, returns NULL. To move
//  to the first frame call zmsg_first(). Advances the cursor.
 zframe_t *
    zmsg_next (zmsg_t *self);

//  Return the last frame. If there are no frames, returns NULL.
 zframe_t *
    zmsg_last (zmsg_t *self);

//  Save message to an open file, return 0 if OK, else -1. The message is 
//  saved as a series of frames, each with length and data. Note that the
//  file is NOT guaranteed to be portable between operating systems, not
//  versions of CZMQ. The file format is at present undocumented and liable
//  to arbitrary change.
 int
    zmsg_save (zmsg_t *self, FILE *file);

//  Load/append an open file into message, create new message if
//  null message provided. Returns NULL if the message could not 
//  be loaded.
 zmsg_t *
    zmsg_load (zmsg_t *self, FILE *file);

//  Serialize multipart message to a single buffer. Use this method to send
//  structured messages across transports that do not support multipart data.
//  Allocates and returns a new buffer containing the serialized message.
//  To decode a serialized message buffer, use zmsg_decode ().
 size_t
    zmsg_encode (zmsg_t *self, char **buffer);

//  Decodes a serialized message buffer created by zmsg_encode () and returns
//  a new zmsg_t object. Returns NULL if the buffer was badly formatted or 
//  there was insufficient memory to work.
 zmsg_t *
    zmsg_decode (char *buffer, size_t buffer_size);

//  Create copy of message, as new message object. Returns a fresh zmsg_t
//  object, or NULL if there was not enough heap memory.
 zmsg_t *
    zmsg_dup (zmsg_t *self);

//  Dump message to stderr, for debugging and tracing.
//  See zmsg_dump_to_stream() for details
 void
    zmsg_dump (zmsg_t *self);

//  Dump message to FILE stream, for debugging and tracing. 
//  Truncates to first 10 frames, for readability; this may be unfortunate
//  when debugging larger and more complex messages.
 void
    zmsg_dump_to_stream (zmsg_t *self, FILE *file);

//  Self test of this class
 int
    zmsg_test (bool verbose);
'''

ffi.cdef(functions)

new = C.zmsg_new
def destroy(m):
    ptop = ffi.new('zmsg_t*[1]')
    ptop[0] = msg
    C.zmsg_destroy(ptop)

recv = C.zmsg_recv

def send(msg, socket):
    ptop = ffi.new('zmsg_t*[1]')
    ptop[0] = msg
    C.zmsg_send(ptop, socket)

size = C.zmsg_size
content_size = C.zmsg_content_size
push = C.zmsg_push
pop = C.zmsg_pop

def append(msg, frame):
    ptop = ffi.new('zframe_t*[1]')
    ptop[0] = frame
    C.zmsg_append(msg, ptop)

add = C.zmsg_add
pushmem = C.zmsg_pushmem
addmem = C.zmsg_addmem
pushstr = C.zmsg_pushstr
addstr = C.zmsg_addstr
popstr = lambda s: ffi.string(C.zmsg_popstr(s))
wrap = C.zmsg_wrap
unwrap = C.zmsg_unwrap
remove = C.zmsg_remove
first = C.zmsg_first
next = C.zmsg_next
last = C.zmsg_last
save = C.zmsg_save
load = C.zmsg_load
encode = C.zmsg_encode
decode = C.zmsg_decode
dup = C.zmsg_dup
dump = C.zmsg_dump
dump_to_stream = C.zmsg_dump_to_stream
test = C.zmsg_test
