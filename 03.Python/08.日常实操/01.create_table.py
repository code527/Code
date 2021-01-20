# -*- coding: utf-8 -*-

def get_index(index):
    if index >= 0 and index <10:
        return '0' + str(index)
    else:
        return str(index)

def create_tables():
    '''
    '''
    sql_template = '''
    CREATE TABLE `card_table_%s`(
      `card_id` varchar(128) NOT NULL COMMENT '卡片id',
  	  `content` varchar(1024) NOT NULL COMMENT '内容json',
  
  	  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  	  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  	  UNIQUE KEY (`card_id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COMMENT = '离线push消息回执统计';
'''
    
    f = open('./tab.sql', 'a')
    
    for i in range(0, 100):
        str = sql_template % (get_index(i))
        f.write(str)
        
    f.close()
    
if __name__ == "__main__":
    create_tables()
