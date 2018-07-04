CREATE TABLE `机器学习_全国` (
  `job_id` int(30) NOT NULL AUTO_INCREMENT,
  `职位名称` varchar(255) DEFAULT NULL,
  `公司名称` varchar(255) DEFAULT NULL,
  `公司链接` varchar(255) DEFAULT NULL,
  `职位链接` varchar(255) NOT NULL,
  `职位月薪` varchar(255) DEFAULT NULL,
  `工作地点` varchar(255) DEFAULT NULL,
  `发布日期` varchar(255) DEFAULT NULL,
  `工作性质` varchar(255) DEFAULT NULL,
  `工作经验` varchar(255) DEFAULT NULL,
  `最低学历` varchar(255) DEFAULT NULL,
  `招聘人数` varchar(255) DEFAULT NULL,
  `职位类别` varchar(255) DEFAULT NULL,
  `岗位职责描述` varchar(3000) DEFAULT NULL,
  `福利标签` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`职位链接`),
  UNIQUE KEY `job_id` (`job_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8