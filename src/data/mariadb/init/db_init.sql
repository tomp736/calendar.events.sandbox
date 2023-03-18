use mydatabase;

CREATE TABLE events (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(255) NOT NULL,
  `summary` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `location` VARCHAR(255),
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
);

CREATE TABLE tasks (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `duration` INT(11) NOT NULL,
  `completed` BOOLEAN DEFAULT FALSE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE event_task (
  `event_id` INT(11) NOT NULL,
  `task_id` INT(11) NOT NULL,
  PRIMARY KEY (`event_id`, `task_id`),
  FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`) ON DELETE CASCADE
);

CREATE TABLE webhooks (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `uid` VARCHAR(36) NOT NULL,
  `endpoint` VARCHAR(255) NOT NULL,
  `event_type` VARCHAR(50) NOT NULL,
  `secret_key` VARCHAR(50) NULL,
  `enabled` BOOL NOT NULL DEFAULT TRUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert the day1 event into the events table
INSERT INTO events (id, uid, summary, description, location, start_time, end_time) VALUES
(1, 'day1', 'Agile Principles', 'Introduction to Agile Manifesto and its principles', 'Online', '2023-03-18 00:00:00', '2023-03-18 01:00:00'),
(2, 'day2', 'Lean Principles', 'Introduction to Lean philosophy and its principles', 'Online', '2023-03-19 00:00:00', '2023-03-19 01:00:00'),
(3, 'day3', 'Scrum Framework', 'Introduction to Scrum framework and its components', 'Online', '2023-03-20 00:00:00', '2023-03-20 01:00:00'),
(4, 'day4', 'Scrum Roles and Artifacts', 'Explanation of Scrum roles and their responsibilities', 'Online', '2023-03-21 00:00:00', '2023-03-21 01:00:00'),
(5, 'day5', 'Scrum Events and Ceremonies', 'Explanation of Scrum events and their purposes', 'Online', '2023-03-22 00:00:00', '2023-03-22 01:00:00'),
(6, 'day6', 'Scrum Implementation', 'Discussion of best practices for implementing Scrum in an organization', 'Online', '2023-03-23 00:00:00', '2023-03-23 01:00:00'),
(7, 'day7', 'Review and Practice', 'Review notes and take practice quiz or exam', 'Online', '2023-03-24 00:00:00', '2023-03-24 01:00:00');

-- Insert the relevant tasks into the tasks table
INSERT INTO tasks (id, title, description, duration) VALUES 
(1, 'Introduction to Agile Principles', 'Watch a video or read an article that provides an overview of Agile principles, such as the Agile Manifesto or the 12 Principles of Agile Software. Take notes on the key concepts and ideas presented, and consider how they apply to your work or your organization.', 60),
(2, 'Agile Principles in Practice', 'Read a case study or watch a presentation that describes how Agile principles were applied in a real-world project or organization. Reflect on the challenges faced and the benefits gained from adopting Agile principles. Discuss with a colleague or mentor how Agile principles could be applied in your own work or organization.', 120),
(3, 'Agile Frameworks', 'Learn about popular Agile frameworks, such as Scrum, Kanban, and Lean. Compare and contrast the different frameworks, and consider which might be most appropriate for your work or organization. Discuss with a colleague or mentor their experience with different Agile frameworks.', 120),
(4, 'Agile Practices', 'Review common Agile practices, such as daily stand-up meetings, sprint planning, and retrospective reviews. Consider which Agile practices might be most beneficial for your work or organization. Brainstorm ideas for implementing Agile practices in your own work or organization.', 60),
(5, 'Assessment and Reflection', 'Take an online quiz or assessment to test your knowledge of Agile principles. Reflect on what you''ve learned throughout the day and identify areas where you''d like to learn more. Set goals for what you''d like to achieve in the remaining days of the SAFe Agile training.', 60);

-- Insert the association between the day1 event and its tasks into the event_task table
INSERT INTO event_task (event_id, task_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5);
