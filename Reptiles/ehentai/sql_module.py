import pymysql
from pymysql.err import IntegrityError


class MySQLConnUrl(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='reptiles'
        )
        self.conn.autocommit(True)

        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.conn.close()

    def fetch_one_url(self, mode='pending', tab_name='ehentai'):
        sql = "SELECT * FROM %s WHERE status = '%s'" % (tab_name, mode)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            return e
        else:
            item = self.cursor.fetchone()
            if not item:
                return None
            if mode == 'pending' or mode == 'aria2':
                if item['check_times'] < 3:
                    sql = "UPDATE %s SET start_time = now(), status = 'ongoing' WHERE id = %d" % (tab_name, item['id'])
                else:
                    sql = "UPDATE %s SET status = 'error' WHERE id = %d" % (tab_name, item['id'])
                    if mode == 'aria2':
                        sql = "UPDATE %s SET status = 'pending', check_times = 0, raw_address = CONCAT('chmode', raw_address) WHERE id = %d" % (
                            tab_name, item['id'])
                    self.cursor.execute(sql)
                    return 'toomany'
            elif mode == 'except':
                sql = "UPDATE %s SET status = 'ongoing' WHERE id = %d" % (tab_name, item['id'])
            try:
                self.cursor.execute(sql)
            except Exception as e:
                self.conn.rollback()
                return e
            else:
                return item

    def update_url(self, item_id, status='finished', tab_name='ehentai'):
        sql = "UPDATE %s SET end_time = now(), status = '%s' WHERE id = %d" % (tab_name, status, item_id)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.conn.rollback()
            return e
        else:
            return item_id

    def reset_url(self, item_id, mode, count=0, tab_name='ehentai'):
        sql = "UPDATE %s SET status = '%s', checktimes=checktimes+%d WHERE id = %d" % (tab_name, mode, count, item_id)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()
            return e
        else:
            return item_id

    def fix_unfinished(self, item_id, img_urls, file_paths, tab_name='ehentai'):
        img_urls = "Š".join(img_urls)
        file_paths = "Š".join(file_paths)
        sql = "UPDATE %s SET failed_links = '%s', failed_paths = '%s', status='except' WHERE id = %d" % (
            tab_name, img_urls, file_paths, item_id)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.conn.rollback()
            return e
        else:
            return 0

    def reset_unfinished(self, item_id, img_urls, file_paths, tab_name='ehentai'):
        failed_num = len(img_urls)
        if failed_num == 0:
            sql = "UPDATE %s SET failed_links = null, failed_paths = null, status = 'finished', endtime = now() WHERE id = %d" % (
                tab_name, item_id)
        else:
            img_urls = "Š".join(img_urls)
            file_paths = "Š".join(file_paths)
            sql = "UPDATE %s SET failed_links = '%s', failed_paths = '%s', status = 'except' WHERE id = %d" % (
                tab_name, img_urls, file_paths, item_id)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.conn.rollback()
            return e
        else:
            return failed_num

    def add_comic_name(self, address, title, tab_name='ehentai'):
        sql = "UPDATE %s SET comic_name = '%s' WHERE raw_address = '%s'" % (tab_name, title, address)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except IntegrityError:
            self.conn.rollback()
            sql_sk = "UPDATE %s SET status = 'skipped' WHERE raw_address = '%s'" % (tab_name, address)
            self.cursor.execute(sql_sk)
            return Exception(title + ' Already download!')
        except Exception as e:
            self.conn.rollback()
            return e
        else:
            return 0

    def fetch_one_gid(self, address, tab_name='ehentai'):
        sql = "SELECT * FROM %s WHERE raw_address = '%s'" % (tab_name, address)
        self.conn.ping(True)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            return e
        else:
            item = self.cursor.fetchone()
            if not item:
                return None
            else:
                return item.get('old_page')


if __name__ == '__main__':
    mq = MySQLConnUrl()
