#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ttxt
import sqlite3

def simplify(word):
    return word.replace(u'ą', u'a').\
            replace(u'Ą', u'A').\
            replace(u'č', u'c').\
            replace(u'Č', u'C').\
            replace(u'ę', u'e').\
            replace(u'Ę', u'E').\
            replace(u'ė', u'e').\
            replace(u'Ė', u'E').\
            replace(u'į', u'i').\
            replace(u'Į', u'I').\
            replace(u'š', u's').\
            replace(u'Š', u'S').\
            replace(u'ų', u'u').\
            replace(u'Ų', u'U').\
            replace(u'ū', u'u').\
            replace(u'Ū', u'U').\
            replace(u'ž', u'z').\
            replace(u'Ž', u'Z')

def main():
    if len(sys.argv) < 3:
        print '%s input output' % __file__
        return

    words = ttxt.read(sys.argv[1])

    con = sqlite3.connect(sys.argv[2])

    cursor = con.cursor()

    cursor.execute("""CREATE TABLE enwords (
        id INTEGER NOT NULL,
        word VARCHAR(128) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (word)
        )""")

    cursor.execute("CREATE INDEX enwords_word_idx ON enwords(word)");

    cursor.execute("""CREATE TABLE ltwords (
        id INTEGER NOT NULL,
        word VARCHAR(128) NOT NULL,
        sword VARCHAR(128) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (word)
        )""")

    cursor.execute("CREATE INDEX ltwords_word_idx ON ltwords(word)");
    cursor.execute("CREATE INDEX ltwords_word_idx_2 ON ltwords(sword)");

    cursor.execute("""CREATE TABLE translations (
        enid INTEGER NOT NULL,
        ltid INTEGER NOT NULL,
         FOREIGN KEY(enid) REFERENCES enwords (id),
         FOREIGN KEY(ltid) REFERENCES ltwords (id)
        )""")

    cursor.execute("CREATE INDEX translations_enid_idx ON translations(enid)");
    cursor.execute("CREATE INDEX translations_ltid_idx ON translations(ltid)");

    # Android specific fix
    cursor.execute("""CREATE TABLE "android_metadata" ("locale" TEXT DEFAULT 'en_US')""")
    cursor.execute("""INSERT INTO "android_metadata" VALUES ('en_US')""")

    keys = words.keys()
    for word in keys:
        if len(words[word]['translations']) > 0:
            cursor.execute('INSERT INTO enwords(word) VALUES(?)', (word,))
            enid = cursor.lastrowid

            for tr in words[word]['translations']:
                cursor.execute('SELECT id FROM ltwords WHERE word = ?', (tr,))
                result = cursor.fetchone()
                ltid = result is not None and result[0] or None
                if ltid is None:
                    cursor.execute('INSERT INTO ltwords(word, sword) VALUES(?, ?)', (tr, simplify(tr)))
                    ltid = cursor.lastrowid

                cursor.execute('INSERT INTO translations(enid, ltid) VALUES(?, ?)', (enid, ltid))

    con.commit()


if __name__ == '__main__':
    main()
