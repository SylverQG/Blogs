# [ComputerNet](https://github.com/SylverQG/Blogs/issues/5)

# 一、概述
1. 计算机性能
   1. 速率（比特每秒bit/s）：比特（bit）：信息论中**信息量的单位**；网络技术中**速率**指的是**数据的传送速率**也称为**数据率**或**比特率**
   2. 带宽（两种不同意义）：
      1. 频域称谓，指信号具有的频带宽度，单位Hz
      2. 时域称谓，表示在单位时间内网络中某信道所能通过的“最高数据率”，单位比特每秒（bit/s）；两者本质一样，一条通信链路的“带宽”越宽，传输的“最高数据率”自然越高
   3. 吞吐量：单位时间内通过某个网络（或信道、接口）的实际数据量。受网络的带宽或网络的额定速率的限制
   4. 时延：时延是指数据（一个报文或分组，甚至是比特）从网络（或链路）的一端传送到另一端所需的时间，有时也成为延迟或迟延
- 发送时延（传输时延）：主机或路由器发送数据帧所需要的时间
```math
   发送时延=\frac{数据帧长度(b)}{发送速率(b/s)}
```
- 传播时延：电磁波在信道中传播一定的距离需要花费的时间
```math
   传输时延=\frac{信道长度(m)}{电磁波在信道上的传播率(m/s)}
```
- 处理时延：主机或路由器在收到分组时需要花费一定的时间进行处理
- 排队时延：结点缓存队列中分组排队所经历的时延（取决于网络当时的通信量）；数据在网络中经历的总时延就是以上四种时延之和
- 注：对于高速网络，提高的仅仅是数据的发送率不是比特在链路上的传播速率
   5. 时延带宽积： $时延带宽积（体积）= 传播时延（长）\times 带宽（截面积）$，以比特为单位的链路长度
   6. 往返时间（RTT）：简单来说，就是两倍传播时延（实际上还包括处理时延，排队时延，转发时的发送时延）
   7. 利用率：信道利用率 $\rightarrow$ 网络利用率（全网络的信道利用率的加权平均值） $D=\frac{D_0}{1-U}, D_0$表示网络空间时的延时， $D_0$表示网络空闲时时延， $U$为利用率， $D$表示网络当前的时延；可见信道利用率并不是越高越好，当某信道的利用率增大时，该信道引起的时延也就迅速增大。 减少方法是增大线路的带宽
2. 计算机网络体系结构
   1. OSI/RM：开放系统互联参考模型（法律上的国际标准）：简称`OSI`
   2. TCP/IP：事实上的国际标准
   3. 协议：为进行网络中的数据交换而建立的规则、标准或约定。三要素：语法（结构和格式），语义（动作），同步（顺序）
   4. 分层的好处
      1. 各层之间是独立的
      2. 灵活性好
      3. 结构上可分割开
      4. 易实现和维护
      5. 能促进标准化工作
   5. 五层体系结构
      1. 应用层：通过应用进程（正在运行的程序）间的交互来完成特定网络应用。（如DNS，HTTP，SMTP，FTP）
      2. 运输层：负责向两台主机中进程之间的通信提供的数据传输服务。（复用和分用）
         1. 传输控制协议TCP：提供面向连接的、可靠的数据传输服务，其数据传输单位是报文段
         2. 用户数据报协议UDP：提供无连接的、尽最大努力的数据传输服务（不保证可靠性），其数据传输单位是用户数据报
      3. 网络层：负责为分组交换网上的不同主机提供通信服务（TCP/IP体系中，分组也叫IP数据报）
      4. 数据链路层：将网络层交下来的IP数据报组装成帧，在两个相邻结点（主机和路由器之间或路由器之间）间的链路上传送帧；每一帧包括数据和必要的控制信息
      5. 物理层：透明地传送比特流（双绞线、同轴电缆、光缆、无线信道等不在物理层）
3. 词语
   1. 实体：任何可发送或接受信息的硬件或软件进程
   2. 协议：控制两个对等实体（或多个实体）进行通信的规则的集合。（水平的）
   3. 在协议控制下，两个对等实体间的通信使得本层能够向上一层提供服务（垂直的）要实现本层协议，还需要使用下面一层所提供的服务
   4. 同一系统相邻两层的实体进行交互（即交换信息）的地方，称为服务访问SAP

# 二、物理层
1. 基本概念
   - 机械特性（接口）
   - 电气特性（电压范围）
   - 功能特性（电压的意义）
   - 过程特征（顺序）
2. 数据通信系统
   一个数据通信系统可划分为三大部分，即源系统（发送端、发送方） $\rightarrow$ 传输系统（传输网络） $\rightarrow$ 目的系统（接收端、接收方）
   - 数据（data）：运送消息的实体
   - 信号（signal）：数据的电气的或电磁的表现
   - 模拟信号或连续信号（analogous）：代表消息的参数的取值是连续的
   - 数字信号或离散信号（digital）：代表消息的参数的取值是离散的
   - 码元（code）：代表不同离散数值的基本波形
3. 信道的基本概念
   信道用来表示向某个方向传送信息的媒体；可以有以下三种基本方式
   1. 单向通信（单工通信）：只能有一个方向的通信而没有反方向的交互（广播）
   2. 双向交替通信（半双工通信）：通信的双方都可以发送信息，但不能双方同时发送（当然也就不能同时接收）这种通信方式是一方发送另一方接收，过一段时间后，可以再反过来
   3. 双向同时通信（全双工通信）：通信的双方可以同时发送和接收信息
4. 信道的极限容量
   1. 信道能够通过的频率范围（码间串扰）：加宽频带
   2. 信噪比：信号的平均功率的噪声的平均功率之比；常记为 $S/N$，并用分贝(dB)作为度量单位。即： $信噪比(dB)=10\log_{10} (S/N)(dB)$
   3. 香农公式：信道的极限信息传输速率 $C=W\log_{2}(1+S/N) (bit/s)$;式中W为信道的带宽（单位Hz），S为信道内所传信号的平均功率，N为信道内部的高斯噪声功率
   4. 香农公式表明：信道的带宽或信道中的信噪比越大，信息的极限传输速率就越高。只要信息传输速率低于信道的极限传输速率，就一定存在某种方法实现无差错传输
5. 信道复用技术
   1. 频分复用（FDM）：所有用户在同样的时间占用不同的资源
   2. 时分复用（TDM）（同步时分复用）：所有用户在不同的时间用同样的频带宽度；（更有利于数字信号的传输）
   3. 以上两种复用方法的优点是技术比较成熟，缺点是不够灵活
   4. 统计时分复用（STDM）（异步时分复用）：动态分配时隙；集中器常使用统计时分复用
   5. 波分复用：光的频分复用
   6. 码分多址（码分多址CDMA）：各用户使用不同的码型，因此各用户之间不会造成干扰。每个站分配的码片序列不仅必须各不相同，并且还必须互相正交（相乘为0，0写为-1，1写为+1）。在使用的系统中是使用为随机序列。
   7. 任何一个码片向量和该码片向量自己的规格内积都是 1；
   8. 任何一个码片向量和该码片反码的向量自己的规格内积都是 -1；
   9. 任何一个码片向量和其他该码片向量自己的规格内积都是 0；
6. 宽带接入技术
   - ADSL（非对称数字用户线）技术：用数字技术对现有模拟电话用户线进行改造。ADSL的极限传输距离取决于数据率和用户线的线经（用户线越细，信号传输时的衰减就越大）
   - 光纤同轴混合网（HFC网）
   - FTTx技术：光纤到户FTTH
7. 例：假定某信道受奈氏准则限制的最高码元速率为20000码元/元。如果采用振幅调制，把码元的振幅划分为16个不同的等级来传送，那么可以获得多高的数据率（b/s）答： $C = R \ast log_{2}{16} = 20000b/s \ast 4 = 80000b/s $
8. 共有4个站进行CDMA通信。4个站的码片序列为
   A. (-1-1-1+1+1-1+1+1)
   B. (-1-1+1-1+1+1+1-1)
   C. (-1+1-1+1+1+1-1-1)
   D. (-1+1-1-1-1-1+1-1)
   现在受到这样的码片序列S：(-1+1-3+1-1-3+1+1)。问哪个站发送数据了发送数据的站发送的是0还是1？
   解：
   $S\cdot A= (+1-1+3+1-1+3+1+1) / 8=1,  A 发送1$
   $S\cdot B= (+1-1-3-1-1-3+1-1) / 8=-1, B 发送0$
   $S\cdot C= (+1+1+3+1-1-3-1-1) / 8=0,  C 无发送$
   $S\cdot D= (+1+1+3-1+1+3+1-1) / 8=1,  D 发送1$

---

# 三、数据链路层
（计算题：1.CRC；2.征用期、最短帧长与时延）
## 要点
1. 两种信道
   1. 点对点信道
   2. 广播信道
2. 链路：从一个结点到相邻结点的一段物理线程（有线或无线），中间没有任何交换结点
3. 数据链路：当需要在一条线路上传送数据时，除了必须有一条物理线路外，还必须由一些必要的通信协议来控制这些数据的传输，把实现这些协议的硬件和软件加到链路上，就构成了数据链路。最常用网络适配器。
4. 帧：协议数据单元
5. 三个基本问题：
   1. 封装成帧：在一段数据前后分别添加首部和尾部进行帧定界（确定帧的界限）
      1. SOH：帧首部，16进制编码01，二进制是00000001
      2. EOT：帧尾部，16禁止编码04，二进制是00000100
   2. 透明传输：解决透明传输问题具体方法：字节填充（或字符填充），发送端的数据链路层在数据中出现控制字符SOH和EOT的前面插入一个转义字符ESC（16进制编码时1B，二进制00011011）
   3. 差错检测：比特在传输过程中可能会产生差错（比特差错）；传输错误的比特占所传输比特总数的比率称为误码率（BER）
   - 循环冗余码CRC：CRC运算就是在数据M的后面添加供差错检测用的n位冗余码
   - n位荣誉码得出方法：用二进制的模2运算进行 $2^n$ 乘M(待传送的数据)的运算，这相当于在M后面添加n个0。得到的(k+n)位的数除以事先商定的长度为(n+1)位的除数P，得到的余数(比除数少一位)作为冗余码，数据加上冗余码在除以除数P，得到的余数为0即为无差错
   - 凡是接收端数据链路层接受的帧均无差错（无比特差错）
   - 传输差错：帧丢失、帧重复、帧失序
6. 点对点协议PPP
目前使用得最广泛的数据链路层协议
   1. 特点
      1. 简单
      2. 封装成帧
      3. 透明性
      4. 多种网络层协议（支持，IP、IPX）
      5. 多种类型链路（串行、并行、同步、异步、高速、低速、电、光、动态、静态）
      6. 差错检测
      7. 检测连接状态
      8. 最大传送单元（MTU）
      9. 网络层地质协商
      10. 数据压缩协商
   2. 不(需要|支持)的功能
      1. 纠错（不可靠传输）
      2. 流量控制（TCP）
      3. 序号（不可靠传输，在无线时可用）
      4. 多点线路（不支持一主对多从）
      5. 半双工或单工链路（只支持双工）
   3. 组成
      1. IP数据报封装到串行链路的方法
      2. 链路控制协议LCP：用来建立、配置和测试数据链路连接
      3. 网络控制协议NCP：其中的每一个协议支持不同的网络层协议
7. 局域网数据链路层
   1. 局域网的拓扑：星形网，环形网，总线网
   2. 静态划分信道：频分复用、时分复用、波分复用、码分复用；动态媒体接入控制又称作多点接入：随机接入、受控接入、如多点线路探询/轮询
   3. 以太网的两个标准：`DIX Ethernet V2`和 `IEEE 802.3`
   4. CSMA/CD（载波监听多点接入/碰撞检测）协议
      1. 以太网采用的措施
         1. 用较为灵活的无连接的工作方式（不进行编号，不要求对方发回确认）
         2. 曼彻斯特编码（一分为二）
      2. 多点接入：总线型网络
      3. 载波监听（检测信道）
      4. 碰撞检测（冲突检测）
      5. 争用期（碰撞窗口）
      6. 最短有效帧长度为64字节
      7. 强化碰撞：认为干扰信号
      8. 帧间最小间隔为 9.6 微秒，相当于 96 比特时间
   5. 以太网的信道利用率
      1. 成功发送一个帧占用信道的时间 T(发送帧需要的时间，由帧长除以发送速率得出) + $\tau$ (单程端到端传播时延)
      2. 参数 a: $a=\frac{\tau}{T_0}$ a越小越好，以太网的帧长度不能太短
      3. 极限信道利用率 $S_{max}=\frac{1}{1+\alpha}$ 只有当a远小于1才能得到尽可能高的极限信道利用率
8. 要发送的数据为101110。才用CRCD生成多项式是 $P(X)=X^3+1$ 试求应该添加在数据后面的余数
答：作二进制除法，101110 000 10011 添加在数据后面的余数是 011

## 总结
1. 功能：为网络层提供服务、链路管理、帧定界、帧同步与透明传输、流量控制和差错控制
   1. 无确认的无连接服务：如以太网
   2. 有确认的无连接服务：如无线通信
   3. 有确认的面向连接服务：通信要求（可靠性、实时性）较高的场合
   4. 注：有链接就一定要确认
指的是接收方应当能从接收到的二进制比特流中区分出帧的起始和终止

2. 组帧：主要解决帧定界、帧同步与透明传输等问题
   1. 字符技术法：在帧头部使用一个技术字段来表明帧内字符数（此字段也在技术范围内）
   2. 首位定界法：
      1. 概念：使用特定字符或比特模式定界帧的开始和结束
      2. 字符填充：在数据中的特殊字符前面用转义字符（ESC）填充加以区分
      3. 比特填充：使用一个特定的比特模式，即0111110（FLAG）来标志一段帧的开始和结束；容易由硬件来实现，性能好
   3. 违规编码法：信号传输过程中采用违规的编码来表示帧的起始和终止（曼彻斯特编码中，采用高-高或低-低的违规方式来定界帧）
3. 差错控制：分为位错和帧错，主要解决方法由自动重传（ARQ）和前向纠错（FEC）
   1. 噪声：传输中的差错都是噪声引起的
      1. 随机热噪声：信道固有，可提高信噪比来减少或避免干扰
      2. 冲击噪声：来自外界，不可通过提高信号幅度来避免，是产生差错的重要原因
   2. 检错编码
      1. 奇偶校验码：奇校验，由n-1位信息元和一位校验元组成，在附上一个校验元后，码长位n的码字中"1"的个数为奇数。偶校验可以反推。奇偶校验位只能发现奇数个比特的错误
      2. 循环冗余码（CRC）：要会计算
   3. 纠错编码
      1. 海明码、汉明码：能发现双比特的错误，但只能纠正单比特错；（计算海明码）纠错d位，需要码距位2d+1；检错d位，需要码距d+1
4. 流量控制：限制发送方的数据流量，使其发送速率不超过接收方的接收能力
   1. 停止等待协议：发送方每发送一帧都要等待接收方的应答信号才能发送下一帧
   2. 后退N帧协议（GBN）：发送方一次可发送N帧，按顺序接收，重传从最后一个确认开始（即采用累计确认，如若收到对5号帧的确认意味着接收方收到了5号及5号帧前面的帧）
   3. 选择重传（SR）：发送方一次可发送N帧，可以不按顺序接收，重传没有确认的帧
      1. 发送窗口大小>1，接收窗口大小>1
      2. 接收窗口不超过序号范围的一般（避免接收窗口向前移动窗口后，新的窗口与旧窗口产生重叠）
   4. 对于窗口大小为n的滑动窗口，其发送窗口为n-1，即最多可以由n-1帧已发送大没有确认
5. 可靠传输：数据链路层通常使用确认和超时重传两种机制来保证可靠传输
数据链路层中流量控制机制和可靠机制是交织在一起的
6. 介质访问：为使用介质的每个点隔离来自同一信道上其他噶结点所传送的信号，以协调活动节点的传输
   1. 用来决定广播信道中信道分配的协议属于数据链路层的一个子层，称为戒指访问控制（MAC）子层
   2. 信道划分戒指访问控制：
      1. 频分复用FDM：将多路信号调制到不同频率载波上叠加一个不同的信号使用；使用于传输模拟信号
      2. 时分复用TDM：将物理信道按时间分别若干时间片，轮流个不同的信号使用；适用于传输数字信号
      3. 波分复用WDM：在一根光纤中传输多种不同波长（频率）的光信号
      4. 码分复用CDM：靠不同的编码来区分各路原始信号，如CDMA技术
   3. 随机访问介质访问控制：不采用集中控制方式解决发送信息的次序问题，用户随机发送信息，占用信道全部速率
      1. ALOHA协议：
         1. 纯ALOHA：不检测直接发送，若无确认则等待重发
         2. 时隙ALOHA：将时间划分为若干个等长时隙，按时发送
      2. CSMA协议：
         1. 1-坚持：闲则发送，忙则继续监听
         2. 非坚持：闲则发送，忙则等待一个随机时间再监听
         3. p-坚持：闲则以概率p发送，1-p等待下一个时隙；忙则等待一个随机时间再监听
      3. CSMA/CD协议（载波侦听多路访问/碰撞检测）
         1. 流程：先听后发，边听边发，冲突停发，随机重发
         2. 碰撞解决：采用二进制指数退避算法来解决碰撞问题（即在第i(i<10)次碰撞后，站点会在0~2的(i-1)次方之间随机选择一个数M，等待M倍的争用期再发送数据。在达到10此碰撞后，随机数的区间固定在最大值1023上，以后不再增加，如果连续超过16次冲突，则丢弃）
         3. 冲突检测时间（即争用期）是指信号在最远两个端点之间往返传输的时间
            1. 最短帧长等于在争用期时间内发送出的比特数
            2. 只有经过争用期之后没有检测到碰撞，才能肯定这次发送不会发送碰撞
         4. 有线局域网
         5. 半双工通信
      4. CSMA/CS（CA碰撞避免）协议
         1. 基本思想：发送数据前先广播告知其他结点，在某一段时间内不要发送数据，以免出碰撞
         2. 避免碰撞：预约信道、ACK帧、RTS/CTS帧
         3. 避免碰撞：采用二进制指数退避算法来解决碰撞问题
         4. 无线局域网
         5. 轮询访问介质访问控制：令牌传递协议，以循环的方式轮询每个结点，只有得到令牌的机器才能发送数据，其他必须等待。令牌环网适合负载中的环境
7. 局域网：一种典型的广播信道，在一个较小的范围内，就各种计算机等设备通过双绞线等戒指连接
   1. 考虑到局域网信道质量好
      1. 采用无连接的工作方式
      2. 不对发对发送帧编号、确认
   2. 介质访问控制（决定性）（CSMA/CD、令牌总线和令牌环，前两种用于总线型局域网，第三种用于环形局域网）
   3. IEEE802标准定义局域网的参考模型对应于OSI参考模型的数据链路层和物理层，并将数据链路层拆分为两个子层：逻辑链路控制(LLC)子层和媒体接入控制(MAC)子层
      1. 物理层：信号的编码和译码、比特的接收和传承
      2. MAC子层：向上层屏蔽对物理层访问的各种差异，提供对物理层的统一访问接口，功能：组帧和拆卸帧、比特传输差错检测、透明传输、寻址、竞争处理
      3. LLC子层：建立和释放数据链路层的逻辑连接、提供与高层的接口、差错控制、给帧加序号
   4. 较低延时和较低的误码率
   5. 三种局域网拓扑实现
      1. 以太网（Ethernet）：逻辑拓扑是总线型结构，物理拓扑是星形或拓展星形
         1. `10BASE-T`以太网使用曼彻斯特编码
         2. 信息传播方式：广播式
      2. 令牌环：逻辑拓扑是环形结构，物理拓扑是星形结构
         1. 最坏的情况下，一个结点获得令牌的等待时间等于逻辑环上所有其他结点一次获得令牌，并在令牌持有时间内发送数据帧的时间总和
      3. FDDI：逻辑拓扑是环形结构，物理拓扑是双环结构
   6. 网卡：装有处理器和存储器，是工作在数据链路层的网路组件，有唯一代码，称为介质访问控制(MAC)地址
      1. MAC地址是链路层地址，长度为6字节(48位)，用于唯一标识网络适配器(网卡)
      2. 一台主机拥有多少个网络适配器就有多少个MAC地址
8. 虚拟局域网
   1. 虚拟局域网可以建立与物理位置无关的逻辑组，只有在同一个虚拟局域网中的成员才会收到链路层广播消息
9. 广域网
   1. 在OSI参考模型中，广域网数据链路层控制协议
      1. PPP协议
         1. 定义：使用串行线路通信的面向字节（帧全长是整个字节）的协议，应用在直接连接两个结点的链路上
         2. 面向字节，采用字节填充方式，只支持全双工链路
         3. 提供差错检测但不提供差错纠错，保证无差错接收；不可靠，不使用序列号和确认机制
         4. 三个组成部分
            1. 链路控制协议LCP：用于建立、配置、测试和管理数据链路
            2. 网络控制协议NCP：PPP允许采用多种网络协议层，每个不同的网络层要用一个相应的NCP来配置，为网络层协议建立和配置逻辑连接
            3. 一个将IP数据包封装到串行链路的方法
      2. HDLC协议：面向比特，采用0比特插入法，帧类分为信息帧、监督帧和无编号帧，数据操作方式：正常响应方式（从站在收到主站许可后才能）、异步平衡方式（每一个复合站都可以进行对其他站的数据传输）、异步响应方式（从站无需主站许可）
         1. 信息帧：第一位为0，传输数据，或使用捎带奇数对数据进行确认
         2. 监督帧：第1、2位分别位1、0，流量控制和差错控制，确认、请求重发、请求暂停发送
         3. 无编号帧：链路建立、拆除等多种控制功能
10. 设备
    1. 网桥：
       1. 特点：两个或多个以太网通过网桥连接起来变成一个网段
       2. 类型
          1. 透明网桥（选择的不是最佳路由）：按照自学习算法填写转发表，按转发表转发
          2. 源路由器网桥（选择的是最佳路由）：先发送发现帧，按返回结果转发
    2. 交换机：实际是一个多端口网桥，工作在数据链路层，数据链路层使用武力地址进行转发
       1. 特点：把两个或多个以太网通过网桥连接起来变成一个网段
       2. 类型：
          1. 透明网桥（选择的不是最佳路由）：按照自学习算法填写转发表，按转发表转发
          2. 源路由网桥（选择的是最佳路由）：先发送发现帧，按返回结果转发
    3. 交换机：实际是一个多端口网桥，工作在数据链路层，数据链路层使用武力地址进行转发
       1. 特点：实际是一个多端口网桥
       2. 交换机具有自学能力，学习的是交换表的内容，交换表中存储着MAC地址到端口的映射，即插即用设备
       3. 优点：每个端口结点所占用的带宽不会因为端口结点数目的增加而减少，且整个交换机的总带宽会随着端口结点的增加而增加
       4. 利用交换机可以实现虚拟局域网（VLAN），VLAN不仅可以隔离冲突域，也可以隔离广播域
       5. 交换方式
          1. 直通式：帧在接口后只检查目的地址，几乎马上就被传出去
          2. 存储转发：先将接收到的帧缓存到高速缓存器，检查数据正确性
    4. 相同点：按MAC地址转发，都能隔离冲突率，不能隔离广播率
    5. 交换机比集线器提供更好的网络性能的原因是交换机支持多对用户同时通信

---

# 四、网络层
网络层向上只提供简单灵活的、无连接、尽最大努力交付的数据报服务；网络层不提供服务质量的承诺

1. 虚电路和数据报服务

||虚电路服务|数据报服务|
|----|----|----|
|思路|可靠通信应当由网络来保证|可靠通信应当由用户主机来保证(尽最大努力交付)|
|连接的建立|必须有|不需要|
|终点地址|仅在连接建立阶段使用，每个分组都有终点的完整地址|每个分组使用段的虚电路号|
|分组的转发|属于同一条虚电路的分组均按照同一路由进行转发 |每个分组独立选择路由进行转发(独立发送)|
|当节点出故障时|所有通过出故障的结点的虚电路均不能工作| 出故障的结点可能会丢失分组，一些路由可能会发生变化|
|分组的顺序|总是按发送顺序到达终点|到达终点时不一定按发送顺序|
|端到端的差错处理和流量控制|可以由网络负责，也可以由用户主机负责|由用户主机负责|

2. 虚拟互连网络(IP网)
使用路由器解决各种异构的物理网络连接在一起的问题

3. 分类的IP地址

IP地址由**ICANN**进行分配(中国向**APINC**);一个IP地址在**整个互联网范围内是唯一的**

IP地址中的网络号字段和主机号字段:

- A类地址：( $2^{31}$----50%)
  - 网络号全0表示本机，全1表示环回测试。---- $2^7 -2$
  - 网络号全0表示本主机的网络地址，全1表示所有主机。---- $2^{24} -2$
- B类地址：( $2^{30}$----25%)
  - 网络号（128.0.0.0 不可用）---- $2^{14} -1$
  - 主机号跟A类一样 ---- $2^{16} -1$
- C类地址：( $2^{31}$----12.5%)
  - 网络号（ 192.0.0.0 不可用）---- $2^{21} -1$
  - 主机号（同上）---- $2^8 -2$

ABC都是单播地址

4. IP地址与硬件地址
   1. 物理地址是数据链路层和物理层使用的地址；IP地址是网络层和以上各层使用的地址，是一种逻辑地址。使用IP地址是隐藏各种底层网络的的复杂性问题而便于分析和研究问题
   2. 数据链路层看不到数据报的IP地址
   3. 路由只根据目的地址的IP号进行路由选择
5. ARP和RARP
   1. ARP：IP地址转换成MAC地址
   2. 请求是广播，相应是单播
6. IP数据报
   1. 不超过576字节
   2. 标识，标志，片偏移：用于分片
   3. TTL（跳数限制）：在经过路由器的时候才减1
   4. 首部检验和：占16位
   5. 常用协议

|协议名|ICMP|IGMP|TCP|UDP|
|----|----|----|----|----|
|协议字段值|1|2|6|17|

7. IP层转发分组的流程
   1. 从一个路由器转发到下一个路由器（目的网络地址，下一跳地址）
   2. 特定的主机路由: 对特定的目的指明一个路由，方便控制网络和测试网络
   3. 默认路由(0.0.0.0): 下一跳路由器的地址不在IP数据报里，而在MAC帧里（转位MAC地址）
   4. 分组转发算法：提取目的的主机的IP地址，得出目的网络地址 $\rightarrow$ 直接交付 $\rightarrow$ 特定主机路由 $\rightarrow$ 下一跳路由 $\rightarrow$ 器默认路由 $\rightarrow$ 转告转发分组出错
8. 划分子网
   1. IP地址：{网络号，子网号，主机号}
   2. 推荐子网掩码中选用连续的1
9. CIDR
   1. IP地址：{网络前缀 / 主机号}
10. 路由聚合
11. ICMP应用
    1. Ping:回送请求和回答报文，没有经过TCP和UDP
    2. Tracert:时间差错报文和终点不可达报文
12. 路由选择协议
    1. 策略
       1. 静态路由选择策略（非自适应路由选择）
       2. 动态路由选择策略（自适应路由选择）
    2. AS
       1. IGB（内部网关协议）：RIP（基于距离向量的路由选择）和OSPF；域内路由选择
       2. EGB（外部网关协议）：BGP-4；域内路由选择
13. IP多播
    1. IP多播所传递的分组需要使用多播IP地址
    2. 多播数据报使用D类地址作为目的地址
14. VPN
    1. 专用地址(可重用地址)包括10/8；172.16/12；192.168/16
    2. 利用隧道技术实现VPN
15. NAT
    1. 安装在路由器上
    2. 将本地地址转为全球IP地址
16. 已知A的IP地址，但不知其MAC地址，欲将数据发送给A，则需要使用ARP协议
17. 网络层的核心功能是路由
18. 路由器在OSI涉及网络层
19. IPv4网络支持的传播方式有单播、广播、多播
20. 伪首部的功能是校验数据
21. RIP路由协议描述正确的是采用距离向量算法
22. 在计算机局域网的构件中，本质上与中继器相同的是集线器。
23. 在物理层扩展 局域网 是集线器。在数据链层扩展局域网是网桥。
24. 10.0.0.0 到10.255.255.225、 172.16.0.0 到 172.31.255.255、 192.168.0.0到 192.168.255.255三个地址段属于专用地址.

25. 202.195.256.31 、65.138.75.0和221.25.55.255都属于不正确的主机IP地址

26. 某单位规划网络需要1024个IP地址，若采用无类型域间路由选择CIDR机制，起始地址为192.24.0.0. 则该网络的掩码为255.255.252.0
27. RIP允许一条路径最多只能包含15个路由器。

28. OSPF最主要的特征就是使用链路状态协议。

29. 192.168.1.14不属于子网192.168.15.19/28的主机地址

30. CSMA/CD 协议的工作过程。
答:对CSMA/CD协议的工作过程通常可概括为“发前先听、边发边听、冲突停发、随机重发”。
CSMA/CD协议的工作过程详述如下:某站点想要发送数据，必须首先侦听信道， 
如果信道空闲，立即发送数据并进行冲突检测;
如果信道忙，继续侦听信道，直到信道变为空闲，发送数据并进行冲突检测;
如果站点在发送数据过程中检 利到冲突，立即停止发送数据并等待随机长的时间， 
重复上述过程。

31. 网络的互连设备有哪些?分别有什么作用和工作在什么层次?
答:中继器工作在物理层，功能是对接收信号进行再生和发送，从而增加信号传输的距离。
集线器是一种特殊的中维器，可作为多个网段的转接设备。
网桥工作于数据链路层，不但能扩展网络的距离或范围，而且可提高网 络的性能、可靠性和安全性。
路由器工作于网络层，用于连接多个逻辑上分开的网络。
桥路器是种结 合桥接器 (bridge) 和路由器(router) 两者功能的设备，它控制从一个网络组件到另一个网络组件(此时充当桥接器)和从网络到因特网(此时充当路由器)的传输。
网关又叫协议转换器，工作于网络层之上，可以支持不同协议之间的转换，实现不同协议网络之间的互连。主要用于不同体系结构的网络或者局域网与主机系统的连接。


## 总结
1. 功能: 
   1. 使用IP 协议把异构网络互连、路由与转发、拥塞控制
   2. IP协议提供的是不可靠服务，但其服务的上层协议为了规避这些不可靠的因素，有些协议就会自己设计机制从而保证自已传输的内容可靠。
2. 流量控制与拥塞控制的区别:
   1. 流量控制往往是指在发送端和接收端之间的点对点通信量的控制
   2. 拥塞控制必须确保通信子网能够传送待传送的数据，是一个全局性的问题:包括开环控制(设计时事先考虑)闭环控制。
      1. 开环控制。设计网络时事先将有关发生拥塞的因素考虑周到，力求不产生拥惠。是种静态的预防方法，系统运行后不再需要修改。理解:无需对当前网络状况的反馈。
      2. 闭环控制。 采用监控网络系统去监视，及时检测到哪里发生拥塞，然后将拥高信息传到合适的地方，以便调整网络系统的运行。是基于反馈环路的概念，是种动态的方法。
3. 路由算法:
   1. 静态:网络管理员手工配置路由信息
   2. 动态:通过路由器间彼此交换的信息来构造路由表
      1. 距离-向量路由算法: 路由表保存了到达每个目的地址的已知最佳距离和下一步的转发地址 (IP地址)
         1. 所有结点都监听从其他结 点传来的路由选择更新信息， 以下情况更新它们的路由选择表:
            1. 被通告一条新的路由，该路由在本结点的路由表中不存在，此时本地系统加入这条新的路由:
            2. 发送来的路由信息中有一条到达某个目的地的路由，该路由比当前使用的路由有较短的距离。
         2. 慢收敛导致发送路由器回路。
         3. Bellman-Ford算法，容易产生环路、无穷大的问题，需要配合防环机制
      2. 链路状态路由算法
         1. 要求每个参与该算法的结点都有完全的网络拓扑信息，它们执行下述两项任务:
            1. 主动测试所有邻接结点的状态
            2. 定期将链路状态传播给所有其他的结点(路由结点)
         2. 每当链路状态报文到达时，路由结点便使用这些状态信息去更新自己的网络拓扑和状态“视野图”，利用**Dijsktra最短略径算法**重新计算路由，即从单的源出发计算到达所有目的结点的最短路径。
      3. 比较:
         1. 距离-向量路由算法的每个结点仅为直接邻居提供从自己到网络中所以其他结点的最低费用估计.
         2. 链路状态路由算法中，每个结点通过广播的方式与所有其他节点交谈，但仅高数它们与它直接相连的转路的费用。
         3. 距离-向量路由算法可能遇到环路等问题。
4. 层次路由:
   1. 概念:将互联网分成许多较小的自治系统，系统有权决定自己内部采用什么路由协议
   2. 协议:
      1. 内部网关协议 (IGP) :自治系统内部使用的网关协议，如RIP、 OSPF
      2. 外部阿关协议 (EGP): 自治系统之间使用的网关协议，如BGP4 
   3. 好处: 使每个区域内部交换路由信息的通信量大大减小

5. 路由选择
路由选择分为直接交付和间接交付（通过判断分组的目的IP地址和该路由器的接收端口的IP地址是否属于同一个子网来进行判断）
   1. 直接交付：发送站与目的站在同一网段内，不涉及路由器
   2. 间接交付：发送站与目的站不在同一网段内，间接交付的最后一个路由器肯定是直接交付

6. IPv4
![IPv4](https://raw.githubusercontent.com/SylverQG/picrepo/main/ChromeBook_Pic/IPv4.png)

   1. 网络地址转换（NAT）：实现专用网络地址和公用网络地址之间的相互转换，对外隐藏内部管理的IP地址，使得整个专用网只需要一个全球IP地址，就可以让多台主机同时访问
   2. 私有IP地址：只用于LAN，不用于WAN，只有本地意义
      1. A类私有地址：10.0.0.0/8，范围是：10.0.0.0 ~ 10.255.255.255
      2. B类私有地址：172.16.0.0/12，范围是：172.16.0.0 ~ 172.16.255.255
      3. C类私有地址：192.168.0.0/16，范围是：192.168.0.0 ~ 192.168.255.255
   3. NAT看到了端口，所以在传输层
   4. 子网划分：采用子网掩码对物理子网再一次进行子网划分，IP地址 = {<网络号>，<子网号>，<主机号>}
      1. 流程：传来的IP数据报，根据网络号，找到连接在本单位网络上路由器，然后此路由器再按照目的网络号和子网号找到目的子网，最后交付给目的主机。
      2. 要使用子网， 必须配置子网掩码。一个B类地址的默认子网掩码为255.255.255.0，如果B类地地址的子网占两个比特，那么子网掩码为 11111111 111111111 11000000 00000000 也就是255.255.192.0。
      3. 子网掩码: 为了告诉主机或路由器对一个A类、B类、C类网络进行了子网划分，使用子网掩码表达新原网络中主机号的借位。
      4. 计算机只需要将 IP地址和其对应的子网掩码逐位”与“，就可得出对应子网的网络地址。
   5. 无分类编址 CIDR: 消除了传统A类、B类和C类地址以及划分子网的概念，使用网络前缓和主机号来对IP址进行编码，网络前缀的长度可以根据需要变化，IP地址={<网络前缀号>，<主机号>}
      1. CIDR的记法上采用在IP地址后面加上网络前缀长度的方法，例如128.14.35.7/20 表示前20位为物络前缀
      2. 这种通过使用网络前缀来减少路由表项的方式称为路由聚合，也称为构成超网
   6. 路由聚合:
      1. 概念:将网络前缀都相同的连续的IP地址组成“CIDR地址块“
      2. 目的:使得一个地址块可以表示很多地址，减少路由表表项和路由器间的信息交换
      3. 方法:把一串IP地址都写为二进制表示，取最长的公共前缀作为网络号
   7. 协议
      1. 地址解析协议ARP: 对于特定的IP地址，查询其对应的物理地址
         1. 工作在网络层
         2. 每个主机都设有一个 ARP高速缓存，存放ARP表(本局域网 上各主机和路由器的IP地址到MAC地址的映射表)，并使用ARP协议动态维护。
         3. ARP请求分组是广播发送的，ARP 响应分组是单播(即一个源地址发送到一个目的地址)
         4. 在通信过程中，IP数据报的源地址和目的地址始终不变，而MAC地址随着链路的改变而改变
         5. 工作原理
            1. 主机A打算向本局域网的主机B发送IP数据报
            2. 先查找 ARP表中是否有B的IP地址，如果有，就能查出MAC地址，完成传输
            3. 如果ARP表中没有，主机A发送MAC地址为FF-FF-FF-FF-FF-FF的帧广播ARP请求分组
            4. 主机B收到该ARP请求后，会想主机A发送响应ARP, 分组中包含B的IP与MuC地址映射关系
            5. A收到该映射关系后，写入A的ARP表中，然后按照查到的MAC地址，发送MC帧
      2. 动态主机配置协议DHCP: 给网络中的主机动态的分配IP地址
         1. 应用层协议，基于UDP，通过客户/服务器方式工作的
      3. 网际控制报文协议 ICMP:用来给主机或路由器报告差错和异常情况，分为差错报告报文和询问报文两类。
         1. IP层协议
         2. ICMP差错报告报文
            1. 终点不可达:当路由器或主机不能交付该数据报时向终点发送
            2. 源点抑制:拥塞丢弃数据报，向源点发送
            3. 时间超过:路由器收到生存T为零的数据报时，丢弃该数据报井向源点发送该报文
            4. 参数问题:路由器或主机收到的数据报的首部中有的字段不正确，丢弃并向源点发送该报文
            5. 改变路由(正定向):路由器把改变路由报文发送给主机，让主机知道下次应将数据发 送给另外的路由器(可通过更好的路由)
         3. ICMP询问报文
            1. 回送请求和回答报报文(例PING)
            2. 时间戳请求和回答报文
            3. 掩码地址请求和回答报文
            4. 路由器询问和通告报文
         4. 不应发送ICMP差错报告报文的几种情况:
            1. 对ICMP差错报告报文不再发送ICMP差错报告报文
            2. 对第一个分片的数据报片的所有后续数据报片都不发生ICMP差错报告报文
            3. 对具有组播地址的数据报都不发送ICMP 差错报告报文
            4. 对具有特殊地址(如127.0.0.0或0.0.0.0)的数据报不发送ICMP差错报告报文
         5. ping：使用ICMP回送请求和回答报文，工作在应用层
         6. traceroute: 使用ICMP时间超过报文，工作在网络层
7. IPv6:首部40B，地址长度16B，从根本上解决Ipv4地址耗尽的问题，
   1. 特点:
      1. 更大的地址空间，128 位，IPv4 为32位
      2. 扩展的地址层次结构
      3. 灵活的首部格式
      4. 改进的选项
      5. 允许协议继续扩充
      6. 支持即插即用(即自动配置)
      7. 支持资源的预分配
      8. IPv6只有在包的源结点才能分片，是端到端的。传输路径中的路由器不能分片，所以在一般的意义上讲，IPv6不允许分片。
      9. 增加安全性。
      10. 不提供校验和字段。
   2. 压缩方式:
      1. 省略前导零: 1050:0000:0000:0000:0600:326b 可表示为1050:0:0:0:5:600:300c:326b 
      2. 通过使用双冒号(:) 代替一系列零来指定IPv6 地址: 1A22:120D:0000:0000:72A2:0000:0000:00C0可表示为1A22:120D:72A2:0000:000O:00C0
         1. 注意:双冒号(:)在一个地址中只能出现一次，也就是说有多处相邻的0时，只能用(:)代表其中一处。
8. 路由协议：功能为获取网络拓扑信息、构建路由表、在网络中更新路由信息、选择到达每个目的网络的最优路径、识别一个网络的最优路径、识别一个网络的无环通路等
   1. 路由收敛: 指当路由环境发生变化后，各路由器调整自己的路由表以适应网络拓扑结构的编号，最终达到稳定状态
   2. 自治系统(AS):在单一的技术管理下的一组路由器。
   3. 内部网关协议IGP
      1. RIP协议: 基于距离一向量路由选择协议，使用UDP,与相邻路由器交换整个路由表
         1. 应用层协议，使用UDP传输数据:
         2. 最大跳数为15,跳数为16则被视为不可达
      2. 0SPF协议: 基于链路状态路由算法，使用IP,与全部路由器交换相部结点链路状态
         1. 网络层协议，直接使用IP数据报发送
         2. 使用Hello分组来保持与其邻居的连接
   4. 外部网关协议EGP:
      1. BGP协议: 基于路径-向量路由选择协议，使用TCP，寻找的并非最佳路由
         1. 使用TCP
         2. 只发送增量路由更新。在建立邻居关系后，路由器会将自己的全部路由信息告知邻居，此后如果路由表发生了变化只将增量/更新部分发送给够
         3. BGP交换的路由信息是到达某个目的网络可络所要经过的各个自治系统序列而不仅仅是下一跳
9. IP组播:在发送者和每一接收者之间实现点对多点网络连接，应用UDP协议，使用D类地址。
   1. D类地址(即组播地址)范围: 224. 0.0.0 ~ 239. 255.255.255
   2. IGMP协议:使路由器知道组播成员的信息
   3. 避免路由环路:构造组播转发树
10. 移动IP:支持移动性的因特网体系结构
    1. 概念:移动节点以固定的网络IP地址，实现跨不同网段的漫游功能
    2. 组成:移动结点、本地代理、外部代理
    3. 主机离开归属地时，既不能直接接收分组，也不能直接发送分组，通过交换地址来间接接收和发送分组。
11. 路由器:就是一台多个输入输出端口的专用计算机，其任务是连接不同的网络(异构网络)并完成路由转发。
    1. 主要功能:路由选择、分组转发(IP 数据报)
    2. 特点:跨域用来连接异构网络，实现路由转发，能隔离冲突域和广播域，依照IP地址转发
    3. 组成:
       1. 控制部分(路由选择部分) :路由选择处理机，根据路由协议构造与维护路由表
       2. 分组转发部分: 交换结构、一组输入端口和一组输出端口
    4. 路由表用软件实现，转发表用软件或硬件实现。
       1. 路由表具有四个项目:目的网络IP地址、子网掩码、下一跳IP地址、接口
       2. 转发表由路由表得出:目的站、下一跳的MAC地址
    5. 路由表中默认路由的目的地址和子网掩码都是0.0.0.0。
    6. 路由器是第三层设备，向传输层即以上层隐藏下层的具体实现，所以物理层数据链路层、网络层协议可以不同，而网络层以上的高层协议必须相同。

---


# 五、传输层
1. 应用进程间的通信
   1. 面向通信部分的最高层:
   2. 用户功能中的最低层:
   3. 提供应用进程间的逻辑通信:
2. 传输层的端口：
   1. 识别各应用层进程:
   2. 只具有本地意义:
      1. 熟知端口(1~1023)
      2. 注册(或登记)端口(1024~49151)
      3. 动态(或客户、短暂)端口号(49152~65535);
3. TCP
   1. TCP数据报文格式
   ![TCP](https://raw.githubusercontent.com/SylverQG/picrepo/main/ChromeBook_Pic/TCP.png)
   2. 面向字节流的传输服务
   3. 提供一种面向连接的、可靠的数据传输服务，保证了端到端数据传输的可靠性
   4. 服务过程
   ![TCP-1](https://raw.githubusercontent.com/SylverQG/picrepo/main/ChromeBook_Pic/TCP-1.png)
   5. 差错控制：TCP利用差错控制提供可靠性，利用三种简单工具：校验和、确认和重传
   6. 有缓存——作流量控制
   7. 流量控制：通过流量控制来定义发送方在收到接收方的确认报文之前可以发送的数据量。滑动窗口是TCP实现流量控制的关键技术。TCP的滑动窗口同数据链路层讨论的滑动窗口的不同：
      1. TCP的滑动窗口面向字节的，数据链路层的则是面向帧的；
      2. TCP的滑动窗口是可变大小的，数据链路层的则是固定大小。
   8. 滑动窗口的指针的位置
   9. 避免拥塞|拥塞控制
      1. MSS：max segment size 最大分段长度 bit
      2. **慢开始（慢启动）** :在建立连接时，发送方将拥塞窗口大小初始化为一个最大报文段的大小MSS，然后每收到一个接收方的对新报文段确认报文，拥塞窗口的大小就增加一个MSS，即对每一个发送方所发送的新报文段的确认都将使拥塞窗口的大小增加一个MSS。
      3. **拥塞避免算法** :为了避免拥塞窗口过快增长，尽量避免拥塞现象的出现。当拥塞窗口大小达到一个门限值时，便采取拥塞避免算法来改变拥塞窗口的大小，其方法是每收到一个确认报文，拥塞窗口大小增加一个MSS，即使该确认报文是针对多个报文段的，拥塞窗口也只增加一个MSS。“加法增大”是指执行拥塞避免算法后，当收到对所有报文段的确认就将拥塞窗口 cwnd增加一个 MSS 大小，使拥塞窗口缓慢增大，以防止网络过早出现拥塞。 
      4. **快重传** :当收到连续三个ACK就认为丢失然后进行重传
      5. **快恢复**
         1.  当发送端收到连续三个重复的 ACK 时，就重新设置慢开始门限 ssthresh。
         2.  与慢开始不同之处是拥塞窗口 cwnd 不是设置为 1，而是设置为 ssthresh + 3  MSS。 
         3.  若收到的重复的 ACK 为 n 个（n > 3），则将 cwnd 设置为 ssthresh + n  MSS。
         4.  若发送窗口值还容许发送报文段，就按拥塞避免算法继续发送报文段。
         5.  若收到了确认新的报文段的 ACK，就将 cwnd 缩小到 ssthresh。
   10. TCP特点
       1.  进程到进程的通信: (点对点， 每个进程都需要一个连接) 
       2.  流交付服务: (无结构的字节流)
       3.  全双工通信: (发送、接收缓存)
       4.  复用和分用: (发送一-复用， 接收一-分用)
       5.  面向连接的服务:
       6.  可靠的服务。(无差错，不丢失，不重复，按序到达)
   11. 套接字 (socket)
       1.  IP地址加端口号:
       2.  TCP连接:: ={socket1, socket2};


4. UDP
   1. UDP提供的是一种无连接的、不可靠的数据传输方式，在数据传输过程中没有流量控制和确认机制，数据报可能会丢失、延迟、乱序到达信宿。
   2. UDP只是提供了利用校验和检查数据完整性的简单差错控制，属于一种尽力而为的数据传输方式。
   3. UDP数据报文格式
   ![UDP](https://raw.githubusercontent.com/SylverQG/picrepo/main/ChromeBook_Pic/UDP.png)
   4. UDP特点
      1. 无连接: (减少开销和发送时延)
      2. 尽最大努力交付:
      3. 面向报文: (对报文不分拆，不合并)
      4. 没有拥塞控制;
      5. 支持一对一，一对多，多对一，多对多的交互通信:
      6. 首部开销小。(八个字节)
      7. 无编号:
      8. 检验和一加上伪 首部和数据部分:
5. 可靠传输的工作原理
   1. 停止等待协议 (等待确认后 在发送)
      1. 在发送完一个分组后，必须暂时保留已发送的分组的副本。
      2. 分组和确认分组都必须进行编号。
      3. 超时计时器的重传时间应当比数据在分组传输的平均往返时间更长一一些。
   2. 自动重传请求ARQ;
      1. 简单，但信道利用率太低:
   3. 连续ARQ协议
      1. 发送窗口，累积确认(对按序到达的最后一个分组发送确认)