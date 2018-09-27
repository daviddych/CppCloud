

// 服务间通信使用tcp方式，消息头定义如下
#pragma pack(1)
struct sc_msg_head_t
{
    unsigned char ver;
    unsigned char head_len;
    unsigned int  body_len;
    unsigned short cmdid;
    unsigned short seqid;
};
#pragma pack()

enum command_id_t
{
    CMD_WHOAMI_REQ = 0x0001, // 普通app(cli)启动上报自己身份
    CMD_GETCLI_REQ = 0x0002,
    CMD_HUNGUP_REQ = 0X0003,
    CMD_GETLOGR_REQ= 0X0004,
    CMD_EXCHANG_REQ= 0X0005,
    CMD_SETARGS_REQ= 0X0006,
    CMD_GETWARN_REQ= 0X0007,
    CMD_IAMSERV_REQ = 0x0008, // 分布式中心端启动时报上自身身份
    CMD_KEEPALIVE_REQ = 0x0009,
    CMD_BROADCAST_REQ = 0x000A,
    CMD_CLIERA_REQ = 0x000B,
    CMD_TESTING_REQ = 0x000C,

    CMDID_MID = 0x1000,

    CMD_WHOAMI_RSP = 0x1001,
    CMD_GETCLI_RSP = 0x1002,
    CMD_HUNGUP_RSP = 0X1003,
    CMD_GETLOGR_RSP= 0X1004,
    CMD_EXCHANG_RSP= 0X1005,
    CMD_SETARGS_RSP= 0X1006,
    CMD_GETWARN_RSP= 0X1007,
    CMD_IAMSERV_RSP = 0x1008,
    CMD_KEEPALIVE_RSP = 0x1009,
    CMD_BROADCAST_RSP = 0x100A,
    CMD_CLIERA_RSP = 0x100B,
    CMD_TESTING_RSP = 0x100C,
};

static const unsigned char g_msg_ver = 1;
static const unsigned int g_maxpkg_len = (200*1024*1024); // 200M Limit