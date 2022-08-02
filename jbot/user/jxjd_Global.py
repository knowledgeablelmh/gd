from telethon import events
from .. import user
from .. import jdbot
from ..diy.utils import read, write
import re
import requests
@user.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    configs = read("str")    
    M_API_TOKEN = ""
    if "M_API_TOKEN" in configs:
        TempConfigs = configs.split("\n")
        for config in TempConfigs:
            if "M_API_TOKEN" not in config:                
                continue            
            kv = config.replace("export ", "")
            M_API_TOKEN = re.findall(r'"([^"]*)"', kv)[0]
            
    if len(M_API_TOKEN) == 0:
        await user.send_message(event.chat_id,"请先找 @magic_noyify_bot 申请解析token填入青龙变量,关键字为M_API_TOKEN")
        return 
            
    headers = {"token": M_API_TOKEN}
    strText=""
    if event.is_reply is True:
        reply = await event.get_reply_message()
        strText=reply.text
    else:    
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]
    
    if strText==None:
        await user.send_message(event.chat_id,'请指定要解析的口令,格式: jx 口令 或对口令直接回复jx ')
        return    
        
    data = requests.post("http://ailoveu.eu.org:19840/jCommand",
                             headers=headers,
                             json={"code": strText}).json()
    code = data.get("code")
    if code == 200:
        data = data["data"]
        title = data["title"]
        jump_url = data["jumpUrl"]
        url = re.findall("(.*?)&", data['jumpUrl'])
        activateId = re.findall("activityId=(.*?)&", data['jumpUrl'])
        code = re.findall("code=(.*?)&", data['jumpUrl'])
        msg1 = f'【活动名称】 {data["title"]}\n【分享来自】 ({data["userName"]})\n【活动链接】 [长按复制]({data["jumpUrl"]})\n【快捷跳转】 [点击跳转](https://api1.windfgg.cf/jd/jump?url={data["jumpUrl"]})'
        if re.findall("https://cjhydz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
                   msg = f'【CJ组队瓜分变量】\nexport jd_cjhy_activityId="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
                   msg = f'【LZ组队瓜分变量】\nexport jd_zdjr_activityId="{activateId[0]}"'
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index/8882761", data['jumpUrl']):
                   msg = f'【微定制瓜分变量】\nexport jd_wdz_activityId="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxShareActivity/activity/6432842", data['jumpUrl']):
                   msg = f'【LZ分享有礼变量】\nexport jd_fxyl_activityId="{activateId[0]}"'
        elif re.findall("https://lzkj-isv.isvjd.com/wxCollectionActivity/activity2", data['jumpUrl']):
                   msg = f'【M加购任务变量】\nexport M_WX_ADD_CART_URL="{url[0]}"'
        elif re.findall("https://lzkj-isv.isvjcloud.com/drawCenter/activity", data['jumpUrl']):
                   msg = f'【M加购任务变量】\nexport M_WX_ADD_CART_URL="{url[0]}"'
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxDrawActivity/activity/867591", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'
        elif re.findall("cjwx/common/entry.html", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxCollectionActivity/activity2", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'
        elif re.findall("https://lzkj-isv.isvjcloud.com/lzclient", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxDrawActivity/activity", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxDrawActivity/activity", data['jumpUrl']):
                   msg = f'【M转盘抽奖变量】\nexport M_WX_LUCK_DRAW_URL="{url[0]}"'               
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxgame/activity", data['jumpUrl']):
                   msg = f'【通用游戏变量】\nexport WXGAME_ACT_ID="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxShareActivity", data['jumpUrl']):
                   msg = f'【kr分享有礼变量】\nexport jd_fxyl_activityId="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxSecond", data['jumpUrl']):
                   msg = f'【读秒变量】\nexport jd_wxSecond_activityId="{activateId[0]}"'
        elif re.findall("https://jinggengjcq-isv.isvjcloud.com", data['jumpUrl']):
                   msg = f'【大牌联合开卡变量】\nexport DPLHTY="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCartKoi/cartkoi", data['jumpUrl']):
                   msg = f'【购物车锦鲤变量】\nexport jd_wxCartKoi_activityId="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCollectCard", data['jumpUrl']):
                   msg = f'export jd_wxCollectCard_activityId="{activateId[0]}"\n【集卡抽奖变量】'
        elif re.findall("https://lzkj-isv.isvjd.com/drawCenter", data['jumpUrl']):
                   msg = f'【LZ刮刮乐抽奖变量】\nexport jd_drawCenter_activityId="{activateId[0]}"'
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxFansInterActionActivity", data['jumpUrl']):
                   msg = f'【LZ粉丝互动变量】\nexport jd_wxFansInterActionActivity_activityId="{activateId[0]}"'
        elif re.findall("https://prodev.m.jd.com/mall/active/dVF7gQUVKyUcuSsVhuya5d2XD4F", data['jumpUrl']):
                   msg = f'【邀好友赢大礼变量】\nexport yhyauthorCode="{code[0]}"'                   
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", data['jumpUrl']):
                   msg = f'【关注抽奖变量】\nexport jd_wxShopFollowActivity_activityId="{activateId[0]}"'                    
        else:
                   msg = "未检测到变量信息"
        await user.send_message(event.chat_id,msg1+"\n"+msg)
    else:
        await user.send_message(event.chat_id,"解析出错:"+data.get("data"))
