# [DRF](https://github.com/SylverQG/Blogs/issues/12)

# DRF

简单可行的约定，非标准

## 1. 六层表格

| 层          | ✅ 该做的       | ❌ 不该做的  |
| ----------------------- | ----------------------- | ----------------------- |
| **1. Model**      | • 字段定义（CharField, ForeignKey…）<br>• 表关系映射<br>• Meta 配置（db_table, ordering…）<br>• 简单 @property 派生字段<br>• 唯一约束 / 默认值等数据库约束       | • 业务校验<br>• 调用外部接口<br>• 写查询方法以外的逻辑<br>• 事务控制 |
| **2. Serializer** | • 字段声明（哪些字段、读写属性）<br>• 参数校验（validate_* / validate）<br>• 数据结构描述（to_representation）<br>• 简单派生字段（SerializerMethodField）<br>• 嵌套序列化展示关联数据      | • 事务（transaction.atomic）<br>• 创建消息通知（Message / MessageRecord）<br>• 发邮件 / 发短信<br>• 调用第三方接口（支付、开票）<br>• 权限判断<br>• 机构特殊业务规则 |
| **3. ViewSet**    | • 接收请求<br>• 选择 Serializer<br>• 调用 Service<br>• 返回 Response<br>• get_queryset 基础过滤<br>• 分页 / 排序配置      | • 写复杂 SQL / 聚合查询<br>• 调用外部支付网关<br>• 创建 Message / MessageRecord<br>• 写机构特定的 if-else 分支<br>• 事务控制|
| **4. Service**    | • 事务控制（transaction.atomic）<br>• 调用外部接口（支付、开票、短信）<br>• 创建消息通知（Message / 邮件）<br>• 机构特殊规则<br>• 聚合统计 / 报表计算<br>• 多表联动操作（Order + Task 同时更新）<br>• 可被单元测试的纯业务函数 | • 接收 / 返回 HTTP Request/Response<br>• 做参数校验（交给 Serializer）<br>• 决定返回什么状态码（交给 ViewSet）<br>• 分页 / 排序（交给 ViewSet / DRF）<br>• 权限判断（交给 Permission）  |
| **5. Permission** | • 判断用户是否登录<br>• 判断用户是否有机构权限<br>• 判断用户是否有操作权限<br>• 返回 True / False           | • 写业务逻辑<br>• 查业务数据做判断<br>• 返回业务错误信息      |
| **6. Filter**     | • 按字段精确 / 模糊过滤<br>• 按日期范围过滤<br>• 按状态 / 类型过滤<br>• 排序规则定义| • 写聚合统计<br>• 修改原始数据<br>• 做权限判断|

---

## 2. 完整请求链路（加入 Service 后）

```
HTTP Request
    │
    ▼
URL Router ───────── 决定哪个 ViewSet 处理
    │
    ▼
Permission ───────── 身份 + 权限校验
    │
    ▼
ViewSet ──────────── ① 取参 → ② 调 Serializer 校验 → ③ 调 Service 执行业务 → ④ 返回 Response
    │                       │
    ├─ Serializer ────── 校验请求参数、描述返回结构
    │                       │
    └─ Service ──────── 事务、外部调用、通知、规则判断
                            │
                            ▼
                        Model ──── 数据持久化
```

---

## 3. 一句话速记

| 层                   | 一句话                     |
| -------------------- | -------------------------- |
| **Model**      | 定义"数据长什么样"         |
| **Serializer** | 定义"数据怎么验、怎么展示" |
| **ViewSet**    | 定义"请求怎么接、怎么答"   |
| **Service**    | 定义"业务怎么做"           |
| **Permission** | 定义"谁能用"               |
| **Filter**     | 定义"怎么查"               |
