# Quartz 调度表结构（v2.10.7）

> 11 张 `QRTZ_*` 表，标准 Quartz 2.x JDBC JobStore  schema（表名前缀 `QRTZ_`）。DataEase 用其承载数据源同步任务（`core_datasource_task`）等定时调度。

## 域职责

Quartz 是 DataEase 的**双轨调度**之一（另一轨为 Spring `@Scheduled`，见 job-msg-resource.md）。所有表以 `SCHED_NAME` 为调度器命名空间首列，形成以下子模型：

- **作业定义**：`QRTZ_JOB_DETAILS`（作业）+ `QRTZ_TRIGGERS`（触发器主表）
- **触发器类型子表**：`QRTZ_CRON_TRIGGERS`（Cron）、`QRTZ_SIMPLE_TRIGGERS`（简单间隔）、`QRTZ_SIMPROP_TRIGGERS`（自定义属性）、`QRTZ_BLOB_TRIGGERS`（序列化触发器）
- **运行时**：`QRTZ_FIRED_TRIGGERS`（已触发实例）、`QRTZ_PAUSED_TRIGGER_GRPS`（暂停组）、`QRTZ_SCHEDULER_STATE`（调度器心跳）、`QRTZ_LOCKS`（行锁）
- **日历**：`QRTZ_CALENDARS`

> ⚠️ 这些表**仅存在于 migration（MySQL）集**；desktop（H2）集不含 QRTZ 表，桌面版改用 substitute 本地调度（见 index.md §4）。


## Quartz 表
### QRTZ_JOB_DETAILS  （10 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `JOB_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `JOB_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `DESCRIPTION` | `VARCHAR(250)` | NULL |  |  |
| `JOB_CLASS_NAME` | `VARCHAR(250)` | NOT NULL |  |  |
| `IS_DURABLE` | `VARCHAR(1)` | NOT NULL |  |  |
| `IS_NONCONCURRENT` | `VARCHAR(1)` | NOT NULL |  |  |
| `IS_UPDATE_DATA` | `VARCHAR(1)` | NOT NULL |  |  |
| `REQUESTS_RECOVERY` | `VARCHAR(1)` | NOT NULL |  |  |
| `JOB_DATA` | `BLOB` | NULL |  |  |

### QRTZ_TRIGGERS  （16 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `JOB_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `JOB_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `DESCRIPTION` | `VARCHAR(250)` | NULL |  |  |
| `NEXT_FIRE_TIME` | `BIGINT(13)` | NULL |  |  |
| `PREV_FIRE_TIME` | `BIGINT(13)` | NULL |  |  |
| `PRIORITY` | `INTEGER` | NULL |  |  |
| `TRIGGER_STATE` | `VARCHAR(16)` | NOT NULL |  |  |
| `TRIGGER_TYPE` | `VARCHAR(8)` | NOT NULL |  |  |
| `START_TIME` | `BIGINT(13)` | NOT NULL |  |  |
| `END_TIME` | `BIGINT(13)` | NULL |  |  |
| `CALENDAR_NAME` | `VARCHAR(200)` | NULL |  |  |
| `MISFIRE_INSTR` | `SMALLINT(2)` | NULL |  |  |
| `JOB_DATA` | `BLOB` | NULL |  |  |

### QRTZ_SIMPLE_TRIGGERS  （6 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `REPEAT_COUNT` | `BIGINT(7)` | NOT NULL |  |  |
| `REPEAT_INTERVAL` | `BIGINT(12)` | NOT NULL |  |  |
| `TIMES_TRIGGERED` | `BIGINT(10)` | NOT NULL |  |  |

### QRTZ_CRON_TRIGGERS  （5 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `CRON_EXPRESSION` | `VARCHAR(200)` | NOT NULL |  |  |
| `TIME_ZONE_ID` | `VARCHAR(80)` | NULL |  |  |

### QRTZ_SIMPROP_TRIGGERS  （14 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `STR_PROP_1` | `VARCHAR(512)` | NULL |  |  |
| `STR_PROP_2` | `VARCHAR(512)` | NULL |  |  |
| `STR_PROP_3` | `VARCHAR(512)` | NULL |  |  |
| `INT_PROP_1` | `INT` | NULL |  |  |
| `INT_PROP_2` | `INT` | NULL |  |  |
| `LONG_PROP_1` | `BIGINT` | NULL |  |  |
| `LONG_PROP_2` | `BIGINT` | NULL |  |  |
| `DEC_PROP_1` | `NUMERIC(13, 4)` | NULL |  |  |
| `DEC_PROP_2` | `NUMERIC(13, 4)` | NULL |  |  |
| `BOOL_PROP_1` | `VARCHAR(1)` | NULL |  |  |
| `BOOL_PROP_2` | `VARCHAR(1)` | NULL |  |  |

### QRTZ_BLOB_TRIGGERS  （4 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `BLOB_DATA` | `BLOB` | NULL |  |  |

### QRTZ_CALENDARS  （3 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `CALENDAR_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `CALENDAR` | `BLOB` | NOT NULL |  |  |

### QRTZ_PAUSED_TRIGGER_GRPS  （2 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |

### QRTZ_FIRED_TRIGGERS  （13 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `ENTRY_ID` | `VARCHAR(95)` | NOT NULL |  |  |
| `TRIGGER_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `TRIGGER_GROUP` | `VARCHAR(200)` | NOT NULL |  |  |
| `INSTANCE_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `FIRED_TIME` | `BIGINT(13)` | NOT NULL |  |  |
| `SCHED_TIME` | `BIGINT(13)` | NOT NULL |  |  |
| `PRIORITY` | `INTEGER` | NOT NULL |  |  |
| `STATE` | `VARCHAR(16)` | NOT NULL |  |  |
| `JOB_NAME` | `VARCHAR(200)` | NULL |  |  |
| `JOB_GROUP` | `VARCHAR(200)` | NULL |  |  |
| `IS_NONCONCURRENT` | `VARCHAR(1)` | NULL |  |  |
| `REQUESTS_RECOVERY` | `VARCHAR(1)` | NULL |  |  |

### QRTZ_SCHEDULER_STATE  （3 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `INSTANCE_NAME` | `VARCHAR(200)` | NOT NULL |  |  |
| `LAST_CHECKIN_TIME` | `BIGINT(13)` | NOT NULL |  |  |

### QRTZ_LOCKS  （2 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `SCHED_NAME` | `VARCHAR(120)` | NOT NULL |  |  |
| `LOCK_NAME` | `VARCHAR(40)` | NOT NULL |  |  |


