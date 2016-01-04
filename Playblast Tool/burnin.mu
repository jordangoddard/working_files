require python;

use glyph;
use gl;
use glu;
use gltext;
use rvtypes;
use commands;

module: opus_burnin
{
  documentation: """
        Draws the frame number on lower-right part the image
        """;

    global float shot_size;

    \: main (void; int w, int h, 
             int tx, int ty,
             int tw, int th,
             bool stereo,
             bool rightEye,
             int frame,
             [string] argv)
    {
        setupProjection(w, h);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        let _ : op : grey : size : client_shot : shot : show : artist : dept : revision : status : rank: pass: fov : fps : curr_date : _  = argv;

        gltext.size(int(size));

        // Frame Counter

        let text   = "%04d" % frame,
            b      = gltext.bounds("0000"),
            sh     = b[1] + b[3],
            sw     = b[0] + b[2],
            margin = 12,
            x      = w - sw - margin,
            y      = margin,
            g      = float(grey),
            c      = Color(g, g, g, float(op));
        
        glColor(c);
        gltext.color(c);
        gltext.writeAt(x, y, text);

        // Reset text size / make smaller

        gltext.size(int(size) / int(3));

        // Department

        b       = gltext.bounds(dept);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = margin;
        y       = h - int(int(4) * int(margin)) - sh;

        gltext.writeAt(x, y, dept);

        // FOV / camera data

        b       = gltext.bounds(fov);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        y       = h - int(int(4) * int(margin)) - sh;

        gltext.writeAt(x, y, fov);

        // Artist name

        b       = gltext.bounds(artist);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = w - sw - margin;
        y       = h - int(int(2) * int(margin)) - sh;

        gltext.writeAt(x, y, artist);

        // Date and Time

        b       = gltext.bounds(curr_date);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        //x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        x       = w - sw - margin;
        y       = h - int(int(4) * int(margin)) - sh;

        gltext.writeAt(x, y, curr_date);

        // FPS

        b       = gltext.bounds(fps);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        y       = h - margin - margin - sh;

        gltext.writeAt(x, y, fps);

        // Our Shot Number

        b       = gltext.bounds(shot);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        //x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        //y       = int(int(margin) * int(4));
        x       = margin;
        y       = h - margin - margin - sh;

        gltext.writeAt(x, y, shot);

        // Revision

        gltext.size(int(size) / int(2));

        revision = "rev : %s" % revision;
        b       = gltext.bounds(revision);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        //x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        x       = int(int(w) / int(2)) - int(int(12) * margin);
        y       = margin;

        gltext.writeAt(x, y, revision);

        // Client Shot Number

        b       = gltext.bounds(client_shot);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        y       = int(margin * int(4));

        gltext.writeAt(x, y, client_shot);

        // Rank

        rank = "rank : %s" % rank;
        b       = gltext.bounds(rank);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        //x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        x       = int(int(w) / int(2)) + int(int(10) * margin);
        y       = int(int(margin) * int(4));

        gltext.writeAt(x, y, rank);

        // Pass

        pass = "pass : %s" % pass;
        b       = gltext.bounds(pass);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        //x       = int(int(w) / int(2)) - int(int(sw) / int(2));
        y       = margin;

        gltext.writeAt(x, y, pass);

        // Status

        status  = status;
        b       = gltext.bounds(status);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = margin;
        y       = margin;
        //c       = Color(0.9, 0.9, 0, float(op));
        
        //glColor(c);
        //gltext.color(c);

        gltext.writeAt(x, y, status);

        // Show

        b       = gltext.bounds(show);
        sh      = b[1] + b[3];
        sw      = b[0] + b[2];
        x       = margin;
        y       = int(int(margin) * int(4));

        gltext.writeAt(x, y, show);
    }
} 