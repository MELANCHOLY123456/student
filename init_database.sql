-- =====================================================
-- 学生成绩管理系统 - 数据库初始化（明文密码版本）
-- 密码均为明文存储，方便课程实验登录验证
-- =====================================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS student_grade_system
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_grade_system;

-- 删除旧表（如果存在）
DROP TABLE IF EXISTS `score`;
DROP TABLE IF EXISTS `subject`;
DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `user`;

-- =====================================================
-- 表一: user (用户表)
-- =====================================================
CREATE TABLE `user` (
    `user_id`       INT UNSIGNED AUTO_INCREMENT COMMENT '用户ID',
    `username`      VARCHAR(50) NOT NULL COMMENT '登录用户名',
    `password`      VARCHAR(255) NOT NULL COMMENT '登录密码（明文）',
    `role`          ENUM('admin', 'teacher', 'student') NOT NULL DEFAULT 'student',
    `real_name`     VARCHAR(50) DEFAULT NULL,
    `email`         VARCHAR(100) DEFAULT NULL,
    `phone`         VARCHAR(20) DEFAULT NULL,
    `status`        TINYINT NOT NULL DEFAULT 1 COMMENT '0-禁用, 1-启用',
    `created_at`    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- =====================================================
-- 表二: student (学生表)
-- =====================================================
CREATE TABLE `student` (
    `student_id`    INT UNSIGNED AUTO_INCREMENT,
    `user_id`       INT UNSIGNED NOT NULL,
    `name`          VARCHAR(50) NOT NULL,
    `gender`        ENUM('男', '女') DEFAULT NULL,
    `class_name`    VARCHAR(50) NOT NULL,
    `major`         VARCHAR(100) DEFAULT NULL,
    `enrollment_year` YEAR DEFAULT NULL,
    PRIMARY KEY (`student_id`),
    UNIQUE KEY `uk_user_id` (`user_id`),
    CONSTRAINT `fk_student_user` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生表';

-- =====================================================
-- 表三: subject (科目表)
-- =====================================================
CREATE TABLE `subject` (
    `subject_id`    INT UNSIGNED AUTO_INCREMENT,
    `subject_code`  VARCHAR(20) NOT NULL,
    `name`          VARCHAR(100) NOT NULL,
    `credit`        DECIMAL(3,1) NOT NULL DEFAULT 3.0,
    `semester`      VARCHAR(20) DEFAULT NULL,
    `teacher_id`    INT UNSIGNED DEFAULT NULL,
    `description`   VARCHAR(500) DEFAULT NULL,
    PRIMARY KEY (`subject_id`),
    UNIQUE KEY `uk_subject_code` (`subject_code`),
    CONSTRAINT `fk_subject_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `user`(`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科目表';

-- =====================================================
-- 表四: score (成绩表)
-- =====================================================
CREATE TABLE `score` (
    `score_id`      INT UNSIGNED AUTO_INCREMENT,
    `student_id`    INT UNSIGNED NOT NULL,
    `subject_id`    INT UNSIGNED NOT NULL,
    `daily_score`   DECIMAL(5,2) DEFAULT NULL,
    `midterm_score` DECIMAL(5,2) DEFAULT NULL,
    `final_score`   DECIMAL(5,2) DEFAULT NULL,
    `total_score`   DECIMAL(5,2) NOT NULL,
    `gpa_point`     DECIMAL(3,2) DEFAULT NULL,
    `status`        ENUM('draft', 'submitted', 'approved', 'rejected') NOT NULL DEFAULT 'draft',
    `input_by`      INT UNSIGNED NOT NULL,
    `input_time`    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`score_id`),
    UNIQUE KEY `uk_student_subject` (`student_id`, `subject_id`),
    CONSTRAINT `fk_score_student` FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_score_subject` FOREIGN KEY (`subject_id`) REFERENCES `subject`(`subject_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_score_input_by` FOREIGN KEY (`input_by`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成绩表';

-- =====================================================
-- 插入测试数据（明文密码）
-- =====================================================

-- 用户数据（密码都是明文 123456）
INSERT INTO `user` (`user_id`, `username`, `password`, `role`, `real_name`, `status`) VALUES
(1, 'admin001', '123456', 'admin', '系统管理员', 1),
(2, 't2024001', '123456', 'teacher', '张教授', 1),
(3, 's20220101', '123456', 'student', '李明', 1),
(4, 's20220102', '123456', 'student', '王芳', 1),
(5, 's20220103', '123456', 'student', '赵强', 1);

-- 学生数据
INSERT INTO `student` (`student_id`, `user_id`, `name`, `gender`, `class_name`, `major`, `enrollment_year`) VALUES
(1, 3, '李明', '男', '计算机科学与技术2201班', '计算机科学与技术', 2022),
(2, 4, '王芳', '女', '计算机科学与技术2201班', '计算机科学与技术', 2022),
(3, 5, '赵强', '男', '软件工程2202班', '软件工程', 2022);

-- 科目数据
INSERT INTO `subject` (`subject_id`, `subject_code`, `name`, `credit`, `semester`, `teacher_id`, `description`) VALUES
(1, 'CS101', '高等数学', 4.0, '2025-2026-1', 2, '工科数学基础课程'),
(2, 'CS102', '数据结构与算法', 3.5, '2025-2026-1', 2, '计算机专业核心课程'),
(3, 'CS103', '大学英语', 2.0, '2025-2026-1', 2, '公共基础课程');

-- 成绩数据
INSERT INTO `score` (`score_id`, `student_id`, `subject_id`, `daily_score`, `midterm_score`, `final_score`, `total_score`, `gpa_point`, `status`, `input_by`) VALUES
(1, 1, 1, 88.00, 85.00, 90.00, 88.40, 3.70, 'approved', 2),
(2, 1, 2, 92.00, 88.00, 85.00, 88.10, 3.70, 'approved', 2),
(3, 2, 1, 85.00, 82.00, 88.00, 85.90, 3.70, 'approved', 2),
(4, 2, 3, 90.00, 87.00, 92.00, 90.40, 4.00, 'approved', 2),
(5, 3, 2, 78.00, 75.00, 80.00, 78.40, 3.00, 'submitted', 2);

-- 验证查询
SELECT 'user' as table_name, COUNT(*) as count FROM user
UNION ALL SELECT 'student', COUNT(*) FROM student
UNION ALL SELECT 'subject', COUNT(*) FROM subject
UNION ALL SELECT 'score', COUNT(*) FROM score;
