#GET USER ID (before all actions)
cursor=None
cursor.execute("""SELECT user_id FROM piss.user WHERE user_name = '%s'""" % (user_name))
userid = cursor.fetchone()

##RSS
#INSERT (needs rss variable from form.)
cursor.execute("""INSERT INTO piss.rss (rss, user_id) VALUES ('%s','%d')""" % (rss, userid[0]))

#UPDATE (needs rss variable from form.)
cursor=None
cursor.execute("""SELECT rss_id FROM piss.rss WHERE user_id=%d""" % (userid)
rssid = cursor.fetchall()
rssid1 = rssid[0]
rssid2 = rssid[1]
rssid3 = rssid[2]
cursor.execute("""UPDATE piss.rss SET rss='%s' WHERE user_id=%d AND rss_id=%s""" % (rss, userid, rssid))

#SELECT
cursor=None
cursor.execute("""SELECT rss FROM piss.rss WHERE user_id = %d""" % (user_id))
rss = cursor.fetchall()
rss1 = rss[0]
rss2 = rss[1]
rss3 = rss[2]


##Bookmarks
#INSERT (needs url variable from form.)
cursor=None
cursor.execute("""INSERT INTO piss.bookmarks (bookmark, user_id) VALUES ('%s','%d')""" % (bookmark, userid))

#UPDATE (needs url variable from form.)
cursor=None
cursor.execute("""SELECT bookmark FROM piss.bookmarks WHERE user_id = %d""" % (user_id))
bookmark = cursor.fetchone()
bm = cursor.fetchall()
bm1 = bm[0]
bm2 = bm[1]
bm3 = bm[2]
bm4 = bm[3]
cursor=None
cursor.execute("""UPDATE piss.bookmarks SET bookmark='%s' WHERE user_id=%d AND boomark_id=%d """ % (bookmark, userid,bm))


#SELECT
cursor=None
cursor.execute("""SELECT bookmark FROM piss.bookmarks WHERE user_id = %d""" % (user_id))
bookmark = cursor.fetchone()
bm = cursor.fetchall()
bm1 = bm[0]
bm2 = bm[1]
bm3 = bm[2]
bm4 = bm[3]
