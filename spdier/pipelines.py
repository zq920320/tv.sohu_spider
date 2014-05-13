#!/usr/bin/env python
#-*- coding: utf-8 -*-

from util import RedisUtil
from BeautifulSoup import BeautifulSoup
from util.StringUtil import *
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Pipelines:

	def __init__(self, html):
		self.html = html

	def process(self):
		self.get_content()
		pass

	def get_content(self):
		soup = BeautifulSoup(self.html)
		video = {}

		str_config = soup.findAll('script')[3].contents[0]
		video['vid'] = get_config_value(str_config, 'vid')
		video['nid'] = get_config_value(str_config, 'nid')
		video['pid'] = get_config_value(str_config, 'pid')
		video['cover'] = get_config_value(str_config, 'cover')
		video['playlistId'] = get_config_value(str_config, 'playlistId')
		video['cid'] = get_config_value(str_config, 'cid')
		video['subcid'] = get_config_value(str_config, 'subcid')
		video['osubcid'] = get_config_value(str_config, 'osubcid')
		video['category'] = get_config_value(str_config, 'category')
		video['cateCode'] = get_config_value(str_config, 'cateCode')
		video['pianhua'] = get_config_value(str_config, 'pianhua')
		video['tag'] = get_config_value(str_config, 'tag')
		video['tvid'] = get_config_value(str_config, 'tvid')
		video['playerSpaceId'] = get_config_value(str_config, 'playerSpaceId')

		count_url = "http://count.vrs.sohu.com/count/stat.do?videoId=" + video['vid'] + \
		"&tvid=" + video['tvid'] + \
		"&playlistId=" + video['playlistId'] + \
		"&categoryId=" + video['subcid'] + \
		"&catecode=" + video['cateCode'] + \
		"&plat=flash&os=MacOS10.9.2&online=0&type=vms&t=1399992400861.4104111"

		#播放量
		# url = "http://count.vrs.sohu.com/count/stat.do?videoId=1766750&tvid=1265734&playlistId=5696708&categoryId=158&catecode=122102&uid=13950525923672874988&plat=flash&os=MacOS10.9.2&online=0&type=vms&r=http%3A//tv.sohu.com/20140513/n399512567.shtml&t=1399993714380.2917"
		res  = requests.get(count_url)
		str_count = res.text
		video['count'] = str_count[str_count.find("=")+1:]

		#顶踩数
		#这个真心无力吐槽......
		status_url = "http://score.my.tv.sohu.com/digg/get.do?vid=" + video['vid'] + \
		"&type=" + video['cid'] + "&callback=omg&_=1399997399119"
		res = requests.get(status_url)
		str_status = res.text
		str_status = str_status[str_status.find("{"):str_status.rfind("}") + 1]
		status = json.loads(str_status)
		video['upCount'] = status['upCount']
		video['downCount'] = status['downCount']

		#发布时间 | 时长 | 来源 | 简介
		str_cfix = soup.find('div', {'id':'playlist'})
		video['publishTime'] = str_cfix.findAll('li')[0].contents[0][3:-1].strip()
		video['length'] = str_cfix.find('li',{'class':'s h'}).contents[0][3:].strip()
		video['from'] = str_cfix.find('li',{'class':'h'}).contents[0][3:].strip()
		video['intro'] = str_cfix.find('p',{'class':'intro'}).contents[0].strip()

		#评论
		reply_url = "http://access.tv.sohu.com/reply/list/" + \
			video['subcid'] + "_" +\
			video['playlistId'] + "_" +\
			video['vid'] + "_0_10.js"
		# url = "http://access.tv.sohu.com/reply/list/176_5696708_1766750_0_10.js"
		res = requests.get(reply_url)
		str_reply = res.text
		str_reply = str_reply[str_reply.find("{"):str_reply.rfind("}") + 1]
		video['reply'] = json.loads(str_reply)

		#标题
		video['title'] = soup.find('div',{'id':'crumbsBar'}).find('h2')['title']
		video['type'] = soup.find('div',{'class':'crumbs'}).findAll('a')[1].contents[0]


		for i in video:
			print i," : ",video[i]

		# res  = requests.get(url)
		# print res.text

			# soup_res = soup.findAll(True, {'href': re.compile(self._target['grab_url_reg'])})
		# print video['title']
		# print video['type']
		# print video['up']



content = """
<!doctype html>

<html>
<head>


<script type="text/javascript">
  var pvinsight_page_ancestors = '251366993;314606944;399512567';
</script>









<title>火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了 - 搜狐视频</title>
<meta http-equiv="content-type" content="text/html; charset=GBK" />
<meta name="keywords" content="火车;亚洲女子天团;飙舞;广场舞;" />
<meta name="description" content="火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了,火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了在线观看" />
<meta name="robots" content="all" />
<meta name="album" content="V视角中国大妈" />   
<meta name="category" content="新闻" /> 
<meta property="og:videosrc" content="http://share.vrs.sohu.com/1766750/v.swf&autoplay=false" /> 
<meta property="og:url" content="http://tv.sohu.com/20140513/n399512567.shtml"/>  
<meta property="og:type" content="video"/>  
<meta property="og:video" content="http://share.vrs.sohu.com/1766750/v.swf&autoplay=false"/> 
<meta property="og:video:type" content="application/x-shockwave-flash"/> 
<meta property="og:site_name" content="搜狐视频" /> 
<meta property="og:title" content="火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了 - 搜狐视频" /> 
<meta property="og:image" content="http://photocdn.sohu.com/20140513/63a9417b-ebae-4cb2-ba76-394ca788882d_1766750_S_b.jpg" /> 
<meta name="mobile-agent" content="format=html5;url=http://m.tv.sohu.com/20140513/n399512567.shtml">
<script>
(function(){ try{ var u = navigator.userAgent; var m = u.match(/iPhone|iPad|iPod/i); if((location.href.indexOf('#pc')===-1)&&(m || u.indexOf('Android') > -1 || u.indexOf('IEMobile') > -1)){ if (m&&m[0] === 'iPad') { location.href = location.href.replace('http://tv','http://pad.tv'); } else { location.href = location.href.replace('http://tv','http://m.tv'); } } } catch (e) {} })();

(function(){if(/maxthon/.test(navigator.userAgent.toLowerCase())||document.cookie.search(/(^|;\s?)pbb1=1/)>-1)window.location.href="http://tv.sohu.com/upload/browser/error.html"})()

</script>
<script type="text/javascript">
window.__tv_M_setMonitorRate = 0.01;
window.__tv_M = {page:'play_v1'};
!function(n,e){function t(n,e,t){for(var o in e)n[o]=t&&n[o]||e[o]}function o(){function n(){return(0|65536*(1+Math.random())).toString(16).substring(1)}return n()+n()+"-"+n()+"-"+n()+"-"+n()+"-"+n()+n()+n()}function r(n,e,t){if("undefined"==typeof e){var o=new RegExp(";\\s*"+n+"=([^;]+);"),r=o.exec(document.cookie);return r?r[1]:null}var i="";if(t){var a=new Date;a.setFullYear(a.getFullYear()+1),i="; expires="+a.toUTCString()}document.cookie=[n,"=",encodeURIComponent(e),i,"; path=/; domain=.tv.sohu.com"].join("")}n.__tv_M==e&&(n.__tv_M={});var i=n.__tv_M,a=[],u=r("SUV"),c=o();t(i,{rate:.1,debug:0,timeout:6e4,uuid:u,ssid:c,version:"1.0",LOG_SERVER:"http://220.181.11.118/get.gif"},!0),"undefined"!=typeof n.__tv_M_setMonitorRate&&(i.rate=n.__tv_M_setMonitorRate),i.now=function(){return n.performance&&"function"==typeof n.performance.now?parseInt(n.performance.now(),10):(new Date).valueOf()},i.domReady=function(e){var t=n,o=n.document,r=function(){r.flag||(r.flag=!0,"function"==typeof e&&e.call())};if(t.addEventListener)t.addEventListener("DOMContentLoaded",r,!1);else if(o.attachEvent){o.attachEvent("onreadystatechange",function(){"complete"===o.readyState&&(o.detachEvent("onreadystatechange",arguments.callee),r())});var i=function(){if(!r.flag){try{o.documentElement.doScroll("left")}catch(n){return setTimeout(i,1),void 0}r()}},a=!1;try{a=null==t.frameElement}catch(u){}o.documentElement.doScroll&&a&&i()}},i.pingback=function(n){if(n){var e=new Image;e.onload=e.onerror=e.onabort=function(){e=null},e.src=n}},i.log=function(e){e=e||{},t(e,{uuid:u,ssid:c,pass:"",refer:location.href,rate:i.rate,v:i.version},!0),this.page&&(e.page=this.page),n.perfomace&&(e.perf=1),a.push(e)},i.send=function(){var n=function(n){if(i.debug)try{console.debug(n)}catch(e){}},e=function(n){var e=[];for(var t in n)n.hasOwnProperty(t)&&e.push([encodeURIComponent(t),encodeURIComponent(n[t])].join("="));return e.join("&")};if(Math.random()<i.rate){var t=n;n=function(n){t(n);var o=[i.LOG_SERVER,"?",e(n)].join("");i.pingback(o)}}return function(){var e=a.shift();e&&(n(e),a.length&&arguments.callee())}}()}(window),function(n,e){n.onerror=function(){function n(n,e){return t.call(n)===o[e]}var t=Object.prototype.toString,o={string:"[object String]",number:"[object Number]"},r={loseMsg:{"Uncaught ReferenceError: isXunLeiComponentPass is not defined":!0},filter:function(e,t,o){return n(e,"string")&&n(t,"string")&&t.length>0&&n(o,"number")?!!this.loseMsg[e]:!0}};return function(n,t,o){r.filter(n,t,o)||(e.log({type:"catError",msg:n,file:t,line:o}),e.send())}}()}(window,window.__tv_M),function(n,e){var t=function(t){var o=t||{},r=e.now(),i=[],a=null,u=function(){if(null!==a){if(n.clearTimeout(a),a=null,i.length){for(var t=0;t<i.length;t++)i[t]=i[t].join("*");o.list=i.join("~")}e.log(o),e.send()}},c={add:function(n){return i.push([n,e.now()-r]),this},send:function(n){return n&&this.add(n),u(),this},done:function(){return this.send("done")},fail:function(){return this.send("failed")}};return a=n.setTimeout(function(){c.send("timeout")},e.timeout),c};e.tag=function(n){return new t(n)},e.warp=function(n){if(n)for(var t in n)"function"==typeof n[t]&&(n[t]=function(){var o=t,r=n[o];return function(){try{return r.apply(n,arguments)}catch(t){throw e.log({type:"funError",funname:o,msg:t.message}),e.send(),t}}}())},e.addTag=function(){var n=new t({type:"domTag"});return e.domReady(function(){n.done()}),function(e){n.add(e)}}()}(window,window.__tv_M),function(n,e){var t={},o={},r={},i=[],a=function(n){var t=null,o="url="+encodeURIComponent(location.href)+"&page="+encodeURIComponent(e.page);n&&(t=i.shift()),t&&e.pingback(n+o+"&"+t)};e.getScript=function(n,e,t,o,r){var i=document.getElementsByTagName("head")[0]||document.documentElement,a=document.createElement("script");a.src=n,a.charset=t||"",r=r||[];var u=!1;a.onload=a.onreadystatechange=function(){u||this.readyState&&"loaded"!==this.readyState&&"complete"!==this.readyState||(u=!0,e&&e.apply(this,r),a.onload=a.onreadystatechange=null,o&&(a.onerror=o))},i.insertBefore(a,i.firstChild)},e.startCodeListen=function(n,u,c,d){if(!n)return!1;t[n]=e.now();var f=u||4e3,s={needLog:!0};d&&(s=d,s.needLog="undefined"==typeof d.needLog?!0:d.needLog),r[n]=s,s.needLog&&(o[n]=setTimeout(function(){c&&(i.push("code=1&src="+encodeURIComponent(n)+"&time=0"),a(c)),o[n]=null},f))},e.endCodeListen=function(n,u){if(n&&t[n]){var c=t[n]=e.now()-t[n];if(r[n].needLog&&null!==o[n]&&(clearTimeout(o[n]),u&&(i.push("code=1&src="+encodeURIComponent(n)+"&time="+c),a(u))),o.needValue)return c}}}(window,window.__tv_M);
window.__tv_M && __tv_M.addTag('head');
</script>
<link type="text/css" rel="stylesheet" href="http://css.tv.itc.cn/global/global201302.css" />
<link type="text/css" rel="stylesheet" href="http://css.tv.itc.cn/channel/nav_v1.css" />
<link type="text/css" rel="stylesheet" href="http://css.tv.itc.cn/channel/play_v1.css" />
<!--[if IE 6]>
<link type="text/css" rel="stylesheet" href="http://css.tv.itc.cn/channel/play_ie6_v1.css" />
<![endif]-->
<!--[if IE 7]>
<link type="text/css" rel="stylesheet" href="http://css.tv.itc.cn/channel/play_ie7_v1.css" />
<![endif]-->
<script type="text/javascript">
  var vid="1766750";
  var nid = "399512567";
  var pid ="314606944";
  var cover="http://photocdn.sohu.com/20140513/63a9417b-ebae-4cb2-ba76-394ca788882d_1766750_S_b.jpg";  
  var playlistId="5696708";
  var o_playlistId="";
    var cid="25";//一级分类id
  var subcid="176";//二级分类id
  var osubcid="";//二级分类的唯一项
  var category="251366993;314606944;399512567";
  var cateCode="122102;";
  var pianhua = "0";
  var tag = "火车 亚洲女子天团 飙舞 广场舞";
  var tvid = "1265734";
  var playerSpaceId = "";
</script>


</head>
<body>
<script>window.__tv_M && __tv_M.addTag('body_start');</script>
<script>var _sohuHD_page_ads= ['cp_100_1','cp_101_1','cp_102_1','rec_100_1','cp_64_1','cp_103_1','cp_104_1'];
window.CatgoryEnum = {
	1:  { cls: "modComic", order: 0, w1140: 100, w980: 100, wide: 0 },
	2:  { cls: "modTv"   , order: 0, w1140: 40,  w980: 32,  wide: 1 },
	7:  { cls: "modComic", order: 0, w1140: 100, w980: 100, wide: 0 },
	8:  { cls: "modComic", order: 0, w1140: 100, w980: 100, wide: 0 },
	13: { cls: "modMusic", order: 1, w1140: 999, w980: 999, wide: 0 },
	16: { cls: "modComic", order: 0, w1140: 30, w980: 30, wide: 0 },
	24: { cls: "modMusic", order: 1, w1140: 999, w980: 999, wide: 0 },
	25: { cls: "modMusic", order: 1, w1140: 999, w980: 999, wide: 0 },
	0:  { cls: "modComic", order: 0, w1140: 100, w980: 100, wide: 0 }
};

var isWideMod = CatgoryEnum[cid] ? CatgoryEnum[cid].wide : CatgoryEnum['0'].wide;
var vrs_player = "http://tv.sohu.com/upload/swf/20091027/Main.swf";
vrs_player = "http://tv.sohu.com/upload/swf/20140508/Main.swf";
</script>
<script type="text/javascript" src="http://js.tv.itc.cn/kao.js"></script>
<script type="text/javascript" src="http://js.tv.itc.cn/gg.seed.js"></script>
<script type="text/javascript" src="http://js.tv.itc.cn/dict.js"></script>
<script type="text/javascript" src="http://js.tv.itc.cn/site/play/v1/inc.js"></script>
<script>
/*! mm | Date: Tue Nov 12 2013 23:27:31 GMT+0800 (CST) */
!function(){var e=[""],t=document.referrer,n=navigator.userAgent.toLowerCase(),o=n.indexOf("firefox")>=0,i=n.indexOf("msie")>=0&&n.indexOf("opera")<0,a=n.indexOf("safari")>=0,r=function(){var e='<div style="position:absolute;z-index:9999;top:0;left:0;width:100%;height:32px;line-height:32px;background:#ffffe5;border:1px solid #ecdda8;color:#555;text-align:center;font-size:14px;font-family: helvetica,arial,verdana,tahoma,sans-serif;">\u672c\u7f51\u9875\u53d1\u73b0\u672a\u7ecf\u8bb8\u53ef\u88ab\u5d4c\u5957\u64ad\u653e\uff0c\u4e3a\u4fdd\u62a4\u60a8\u7684\u9690\u79c1\u4e0d\u88ab\u7b2c\u4e09\u65b9\u7f51\u7ad9\u7a83\u53d6\uff0c\u9a6c\u4e0a\u4e3a\u60a8\u8df3\u5230\u6b63\u5e38\u7f51\u9875</div>',t=document.createElement("div"),n=document.body||document.head;n.appendChild(t),t.innerHTML=e,setTimeout(function(){top.location=self.location},2e3)};if(parent&&(i&&parent!=document||(o||a)&&parent!=window)&&""!=t&&t!=self.location){for(var f=!1,d=t.match(/\:\/\/([\w\.\-\d]+)\//g),c=0;c<e.length;c++)if("string"==typeof d&&d=="://"+e[c]+"/"||"object"==typeof d&&d.length>0&&d[0]=="://"+e[c]+"/"){f=!0;break}0==f&&r()}}();
</script>

<script>
messagebus.publish('core.loaded_begin');
</script>

<!-- Start:top -->
<div id="hd-navMiniBar" class="areaTop">
  <div class="area clear">
        <h1 class="hd-logoMini">
    <a id="nav_logo" title="搜狐视频" href="http://tv.sohu.com" target="_blank">
        <img width="90" height="23" alt="搜狐视频" src="http://css.tv.itc.cn/channel/header-images/logo-tv-mini.gif">
    </a>
</h1>
<ul id="newplayNavCrumbs" class="hd-subMenu cfix">
    <li><a href="http://tv.sohu.com/" target="_blank" class="txt">首页</a></li>
    <li>
    <div id="newplayNavFloat" class="hd-sBox">
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/movie/">电&nbsp;&nbsp;&nbsp;&nbsp;影</a></dt>
            <dd><a target="_blank" href="http://tv.sohu.com/trailers/">预告片</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1100_p20_p3_u7f8e_u56fd_p40_p5_p6_p73_p80_p9_2d1_p101_p11.html">美国</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1100_p20_p3_u5185_u5730_p40_p5_p6_p73_p80_p9_2d1_p101_p11.html">内地</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1100_p20_p3_u9999_u6e2f_p40_p5_p6_p73_p80_p9_2d1_p101_p11.html">香港</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p11_p2_p3_u97e9_u56fd_p4-1_p5_p6_p70_p80_p9-1_p101_p11.html">韩国</a></dd>
        </dl>
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/drama/">电视剧</a></dt>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1101_p2_p3_u5185_u5730_p4-1_p5_p6_p73_p80_p9-1_p101_p11.html">内地</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/drama/us/">美剧</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1101_p20_p3_u97e9_u5267_p40_p5_p6_p73_p80_p9_2d1_p101_p11.html">韩剧</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/drama/british/">英剧</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1101_p20_p3_u6e2f_u5267_p40_p5_p6_p73_p80_p9_2d1_p101_p11.html">港剧</a></dd>
        </dl>
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/show/">综&nbsp;&nbsp;&nbsp;&nbsp;艺</a></dt>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1106_p2_u97f3_u4e50_p3_p4-1_p5_p6_p70_p80_p9-2_p101_p11.html">音乐</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1106_p2106104_p3_p4_p5_p6_p77_p8_p9_2d1_p101_p110.html">相亲</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1106_p2106113_p3_p4_p5_p6_p77_p8_p9_2d1_p101_p110.html">真人秀</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1106_p2_u8bbf_u8c08_p3_p4-1_p5_p6_p71_p80_p9-2_p101_p11.html">访谈</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p17_p2_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">最新</a></dd>
        </dl>
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/comic/">动&nbsp;&nbsp;&nbsp;&nbsp;漫</a></dt>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1115_p2115103_p3_p40_p50_p6-1_p77_p8_p9.html">冒险</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1115_p2115114_p3_p40_p50_p6-1_p77_p8_p9.html">亲子</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1115_p2115101_p3_p40_p50_p6-1_p77_p8_p9.html">搞笑</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1115_p2115113_p3_p40_p50_p6-1_p77_p8_p9.html">真人</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1115_p20_p3_p40_p51_p6-1_p77_p8_p9.html">剧场版</a></dd>
        </dl>
        <dl>
            <dt><a  target="_blank" href="http://tv.sohu.com/documentary/">纪录片</a></dt>
            <dd><a  target="_blank" href="http://so.tv.sohu.com/list_p1107_p2_u5386_u53f2_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">历史</a></dd>
            <dd><a  target="_blank" href="http://so.tv.sohu.com/list_p1107_p2_u519b_u4e8b_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">军事</a></dd>
            <dd><a  target="_blank" href="http://so.tv.sohu.com/list_p1107_p2_u81ea_u7136_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">自然</a></dd>
            <dd><a  target="_blank" href="http://so.tv.sohu.com/list_p1107_p2_u793e_u4f1a_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">社会</a></dd>
            <dd><a  target="_blank" href="http://tv.sohu.com/s2011/9240/s328641340/">大视野</a></dd>
        </dl>
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/yule/">娱&nbsp;&nbsp;&nbsp;&nbsp;乐</a></dt>
            <dd><a target="_blank" href="http://tv.sohu.com/s2013/yulebobao/">独家爆料</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p113_p2_u660e_u661f_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">明星资讯</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/entnews/">娱乐新闻</a></dd>
        </dl>
        <dl>
            <dt><a target="_blank" href="http://tv.sohu.com/news/">新&nbsp;&nbsp;&nbsp;&nbsp;闻</a></dt>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1122_p2122204_p3_p40_p5_p6_p73_p8_p9.html">国内</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1122_p2122205_p3_p40_p5_p6_p73_p8_p9.html">国际</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1122_p2122102_p3_p40_p5_p6_p73_p8_p9.html">社会</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1122_p2122101_p3_p40_p5_p6_p73_p8_p9.html">军事</a></dd>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p1122_p2122104_p3_p40_p5_p6_p73_p8_p9.html">财经</a></dd>
         
        </dl>
        <dl>
            <dt><a target="_blank" href="http://so.tv.sohu.com/list_p11_p2_p3_p4-1_p5_p6_p70_p80_p9_2d2_p101_p11.html">分&nbsp;&nbsp;&nbsp;&nbsp;类</a></dt>
			 <dd><a target="_blank" href="http://tv.sohu.com/music/">音乐</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/edu/">教育</a></dd>
			<dd><a target="_blank" href="http://tv.sohu.com/vip/">会员</a></dd>
			<dd><a target="_blank" href="http://tv.sohu.com/trends/">星尚</a></dd>
			<dd><a target="_blank" href="http://tv.sohu.com/auto/">汽车</a></dd>
           			 </dl>
       <dl class="end">
			<dt><a target="_blank" href="http://my.tv.sohu.com/">其&nbsp;&nbsp;&nbsp;&nbsp;他</a></dt>
            <dd><a target="_blank" href="http://tv.sohu.com/tech/">科技</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/travel/">旅游</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/hothdtv/">排行榜</a></dd>
            <dd><a target="_blank" href="http://tv.sohu.com/tvhotall/">影视大全</a></dd>

        </dl>
    </div>
    </li>
</ul>
        <!-- nav search -->
<style>
#hd-fBox2,.hd-mUpload{display:none;}
#newplayNavCrumbs{width:138px;}
.areaTop .hd-hotWord{width:312px;overflow:hidden;}
.areaTop .hd-hotWord a{margin-right:5px;}
</style>
<p class="hd-hotWord c-red">
    <a href="http://tv.sohu.com/s2014/ymerwd/?src=play_nav_tj1" style="color:#dd0d0b;" target="_blank">隐秘而伟大</a>
    <a href="http://tv.sohu.com/s2014/bxb/?src=play_nav_tj2" style="color:#dd0d0b;" target="_blank">冰血暴</a>
    <a href="http://tv.sohu.com/s2014/deviousmaids2/?src=play_nav_tj3" style="color:#dd0d0b;" target="_blank">蛇蝎女佣</a>
    <a href="http://tv.sohu.com/s2014/24xszhyt1/?src=play_nav_tj4" style="color:#656465;" target="_blank">24小时</a>
    <a href="http://tv.sohu.com/s2014/rgwan/?src=play_nav_tj5" style="color:#656465;" target="_blank">如果我爱你</a>
    <a href="http://tv.sohu.com/s2013/theblacklist1/?src=play_nav_tj6" style="color:#656465;" target="_blank">黑名单</a>
    <a href="http://tv.sohu.com/s2011/6358/s329815620/?src=play_nav_tj7" style="color:#656465;display:none;" target="_blank">广告狂人</a>

</p>
<div class="hd-soMini">
    <form autocomplete="off" target="_blank" action="http://so.tv.sohu.com/mts" name="sform" method="get" id="sform">
        <input type="text" class="hd-input" value="产科男医生" name="wd" id="gNewSearch">
        <input type="hidden" value="1" name="box">
        <a href="javascript:;"><input type="submit" class="hd-submit" value=""></a>
    </form>
</div>
<!--end nav search-->
        <div class="hd-funMod cfix" id="navLocker">
		</div>
    </div>
</div>
<!-- End:top -->
<script>
messagebus.publish('core.loaded_nav');
window.__tv_M && __tv_M.addTag('nav');
</script>
<div id="crumbsBar">
  <div class="area cfix">
    <div class="left">
      <div class="crumbs"><a href='http://tv.sohu.com/news/'>新闻</a><span class="f-song">&gt;</span><a href ="javascript:sohuHD.searchKey('社会',7,25,1);">社会</a><span class="f-song">&gt;</span>V视角中国大妈</div>
      
      <h2 title="火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了">火车上偶遇“亚洲女子天团”飙舞 人类已无法阻止广场舞了
      </h2>
    
    </div>
    <div class="right">
      <div class="ad"><div id="cp_64_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_64_1');
</script></div>
    </div>
  </div>
</div>
<!-- Start:playerBar -->
<div id="playerBar">
    <div class="area">
        <div id="sohuplayer">
<script>
//for play core
/*http://js.tv.itc.cn/base/plugin/swfobject13052701.js*/
/*! mm | Date: Mon May 27 2013 12:14:47 GMT+0800 (CST) */
typeof _e=="undefined"&&(_e=function(){},window.console&&(_e=function(e){console.info(e)})),window.sohuHDApple={};if(typeof window.ActiveXObject=="function")try{var m=new ActiveXObject("SoHuVA.SoHuDector");m&&m.isSoHuVaReady()&&(sohuHDApple.hasSoHuVA=!0,m.StartSoHuVA())}catch(e){}(function(e,t){sohuHDApple.playerlist=[],sohuHDApple.player=function(){var e=sohuHDApple.playerlist,t=[],n=null,r={};for(i=0;i<e.length;++i){n=document.getElementById(e[i]),r.player=n;if(n){var s=n.tagName;switch(n.tagName){case"OBJECT":case"EMBED":r.type="flash",r.pauseVideo=function(){n.pauseVideo()},r.playVideo=function(){n.playVideo()},r.seekTo=function(e){n.seekTo(e)},r.mute=function(){n.mute()},r.playedTime=function(){return n.playedTime()},r.externalCinema=function(e){n.externalCinema(e)}}}t.push(r)}return t}})(window);var SWFObject=function(e,t,n,r,i,s,o,u,a,f,l){var c=this;if(!document.createElement||!document.getElementById)return;c.movie=c.src=e,c.id=t||"",c.width=n||"auto",c.height=r||"auto",c.ver=i?i.replace(".",","):"7,0,19,0",c.ver=="9,0,145"&&(c.ver="9,0,115"),c.bgcolor=s||"",c.quality=u||"high",c.useExpressInstall=typeof o=="boolean"?o:!1,c.xir=a||window.location,c.redirectUrl=f||window.location,c.detectKey=typeof l=="boolean"?l:!0,c.pluginspage="http://www.macromedia.com/go/getflashplayer",c.type="application/x-shockwave-flash",c.classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",c.codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version="+c.ver,c.objAttrs={},c.embedAttrs={},c.params={},c.flashVarsObj={},c._setAttribute("id",c.id),c.objAttrs.classid=c.classid,c._setAttribute("codebase",c.codebase),c._setAttribute("pluginspage",c.pluginspage),c._setAttribute("type",c.type),c._setAttribute("width",c.width),c._setAttribute("height",c.height),c._setAttribute("movie",c.movie),c._setAttribute("quality",c.quality),c._setAttribute("bgcolor",c.bgcolor)};SWFObject.prototype={getFlashHtml:function(e){var t=this,n=[],r=[];for(var e in t.flashVarsObj)r.push("&",e,"=",t.flashVarsObj[e]);if(document.all){n.push("<object ");for(var e in t.objAttrs)n.push(e,'="',t.objAttrs[e],'"'," ");n.push(">\n");for(var e in t.params)n.push('<param name="',e,'" value="',t.params[e],'" />\n');r.length&&n.push('<param name="flashvars" value="',r.join(""),'" />\n'),n.push("</object>")}else{n.push("<embed "),t.embedAttrs.FlashVars=r.join("");for(var e in t.embedAttrs)n.push(e,'="',t.embedAttrs[e],'"'," ");n.push("></embed>")}return n.join("")},_setAttribute:function(e,t){var n=this;if(typeof e=="undefined"||e==""||typeof t=="undefined"||t=="")return;var e=e.toLowerCase();switch(e){case"classid":break;case"pluginspage":n.embedAttrs[e]=t;break;case"src":case"movie":n.embedAttrs.src=t,n.params.movie=t;break;case"codebase":n.objAttrs[e]=t;break;case"onafterupdate":case"onbeforeupdate":case"onblur":case"oncellchange":case"onclick":case"ondblClick":case"ondrag":case"ondragend":case"ondragenter":case"ondragleave":case"ondragover":case"ondrop":case"onfinish":case"onfocus":case"onhelp":case"onmousedown":case"onmouseup":case"onmouseover":case"onmousemove":case"onmouseout":case"onkeypress":case"onkeydown":case"onkeyup":case"onload":case"onlosecapture":case"onpropertychange":case"onreadystatechange":case"onrowsdelete":case"onrowenter":case"onrowexit":case"onrowsinserted":case"onstart":case"onscroll":case"onbeforeeditfocus":case"onactivate":case"onbeforedeactivate":case"ondeactivate":case"width":case"height":case"align":case"vspace":case"hspace":case"class":case"title":case"accesskey":case"name":case"id":case"tabindex":case"type":n.objAttrs[e]=n.embedAttrs[e]=t;break;default:n.params[e]=n.embedAttrs[e]=t}},_getAttribute:function(e){var t=this;return e=e.toLowerCase(),typeof t.objAttrs[e]!="undefined"?t.objAttrs[e]:typeof getA.params[e]!="undefined"?t.params[i]:typeof getA.embedAttrs[e]!="undefined"?t.embedAttrs[e]:null},setAttribute:function(e,t){this._setAttribute(e,t)},getAttribute:function(e){return this._getAttribute(n)},addVariable:function(e,t){var n=this;n.flashVarsObj[e]=t},getVariable:function(e){var t=this;return t.flashVarsObj[e]},addParam:function(e,t){this._setAttribute(e,t)},getParam:function(e){return this._getAttribute(e)},write:function(e){var t=this;typeof e=="string"?document.getElementById(e).innerHTML=t.getFlashHtml(e):typeof e=="object"&&(e.innerHTML=t.getFlashHtml(e))},writeCode:function(e){var t=this;document.write(t.getFlashHtml())},playerVer:function(){if(document.all){var e=new ActiveXObject("ShockwaveFlash.ShockwaveFlash");e&&(flashVersion=parseInt(e.GetVariable("$version").split(" ")[1].split(",")[0]))}else if(navigator.plugins&&navigator.plugins.length>0){var e=navigator.plugins["Shockwave Flash"];if(e){var t=e.description.split(" ");for(var n=0;n<t.length;++n){if(isNaN(parseInt(t[n])))continue;flashVersion=parseInt(t[n])}}}return{v:flashVersion}}},function(e,t,n){var r=-1,i=!1;document.all&&(i=!0);var s=(new Date).getTime();sohuHDApple.random=function(){return s+=1,s},sohuHDApple.getScript=function(e,t,n,r){var i=document.head||document.getElementsByTagName("head")[0]||document.documentElement,s=document.createElement("script");s.src=e,s.charset=n||"GBK";var o=!1;r&&(s.onerror=r),s.onload=s.onreadystatechange=function(){!o&&(!this.readyState||this.readyState==="loaded"||this.readyState==="complete")&&(o=!0,t&&t(),s.onload=s.onreadystatechange=null,i&&s.parentNode&&i.removeChild(s))},i.insertBefore(s,i.firstChild)},sohuHDApple.cookie=function(e,t,n){if(typeof t=="undefined"){var r=(new RegExp("(?:^|; )"+e+"=([^;]*)")).exec(document.cookie);return r?r[1]||"":""}n=n||{},t===null&&(t="",n.expires=-1);var i="";if(n.expires&&(typeof n.expires=="number"||n.expires.toUTCString)){var s;typeof n.expires=="number"?(s=new Date,s.setTime(s.getTime()+n.expires*24*60*60*1e3)):s=n.expires,i="; expires="+s.toUTCString()}var o=n.path?"; path="+n.path:"",u=n.domain?"; domain="+n.domain:"",a=n.secure?"; secure":"";document.cookie=[e,"=",t,i,o,u,a].join("")},sohuHDApple.getUrlParam=function(e,n){n=escape(unescape(n));var r=new Array,i=null;if(e.nodeName=="#document")t.location.search.search(n)>-1&&(i=t.location.search.substr(1,t.location.search.length).split("&"));else if(typeof e.src!="undefined"){var s=e.src;if(s.indexOf("?")>-1){var o=s.substr(s.indexOf("?")+1);i=o.split("&")}}else{if(typeof e.href=="undefined")return null;var s=e.href;if(s.indexOf("?")>-1){var o=s.substr(s.indexOf("?")+1);i=o.split("&")}}if(i==null)return null;for(var u=0;u<i.length;u++)escape(unescape(i[u].split("=")[0]))==n&&r.push(i[u].split("=")[1]);return r.length==0?null:r.length==1?r[0]:r},function(e,t){var n=t.navigator.userAgent;e.prototype.isMacSafari=/Macintosh/ig.test(n)&&/Safari/ig.test(n)&&!/Chrome/ig.test(n),e.prototype.isMacChrome=/Macintosh/ig.test(n)&&/Safari/ig.test(n)&&/Chrome/ig.test(n),e.prototype.isIpad=/ipad/ig.test(n)||/lepad_hls/ig.test(n)||/SonyDTV/ig.test(n),e.prototype.isIphone=/\(i[^;]+;( U;)? CPU iphone.+Mac OS X/ig.test(n),e.prototype.isIpod=/\(i[^;]+;( U;)? CPU ipod.+Mac OS X/ig.test(n),e.prototype.isIOS=/iphone|ipod|ipad/ig.test(n),e.prototype.isIOSLow=!1,e.prototype.enforceFlash=!1,e.prototype.enforceMP4=!1,e.prototype.switchHtml="",e.prototype.isIOS||(e.prototype.isSBDevice=/MQQBrowser/ig.test(n));if(/iphone|ipod/ig.test(n)){var r=n.indexOf(" OS ")+4,i=parseFloat(n.substring(r,n.indexOf(" ",r)).replace(/_/g,"."));i<4.2&&(e.prototype.isIOSLow=!0)}e.prototype.isSogou=/SE \d+\.X/.test(n),e.prototype.isIEMobile=/IEMobile/.test(n),e.prototype.isAndroid=/android/ig.test(n),e.prototype.isAndroidLow=!1,e.prototype.isAndroidHigh=!1;if(e.prototype.isAndroid){var s=n.match(/\bAndroid\b(.*\d)?;/)||[0,"0.0"];e.prototype.androidVer=s,s=parseInt(s[1].replace(/\./g,"")),s<100&&(s*=10),s<230?e.prototype.isAndroidLow=!0:s>411&&(e.prototype.isAndroidHigh=!0)}}(e,t),e.prototype.eventObj={},e.prototype.bindEvents=function(e,t){e&&t&&(this.eventObj[e]=t)},e.prototype.getFlashHtml=function(n){var s=this,u=[],a=[],f={"#super":"21","#high":"1","#common":"2"};f=f[location.hash]||"",f&&(s.flashVarsObj.co=f),s.flashVarsObj.api_key||(s.flashVarsObj.api_key=sohuHDApple.getUrlParam(document,"api_key"));var l=sohuHDApple.cookie("ch_key");l&&(s.flashVarsObj.ch_key=l),sohuHDApple.cookie("machtml5new")&&(s.isIpad=!0),s.isSBDevice=s.isSBDevice||!s.isIOS&&s.flashVarsObj.enforceMP4||s.isAndroidLow,s.isSBDevice&&(s.isAndroidHigh=!1);var c=!s.checkFlash(x);s.flashVarsObj.enforceHTML5&&(s.enforceHTML5=s.flashVarsObj.enforceHTML5),s.enforceHTML5&&(s.isAndroid=!0);if(!s.enforceFlash&&(s.isIpad||s.isIphone||s.isIpod||s.isIEMobile||s.isAndroid||s.isSBDevice)){s.isIOSLow&&alert("\u60a8\u7684iOS\u7248\u672c\u4f4e\u4e8e4.2,\u8bf7\u5347\u7ea7\u7cfb\u7edf\u7248\u672c\u4ee5\u83b7\u5f97\u66f4\u6d41\u7545\u89c2\u770b\u4f53\u9a8c.");var n="playerbox"+sohuHDApple.random();sohuHDApple.getScript("http://js.tv.itc.cn/base/plugin/mobile13052701.js",function(){s.getHTML5(n)});var h=s.width,p=s.height,d=/^-?\d+(?:px)?$/i;return d.test(h)&&(h+="px"),d.test(p)&&(p+="px"),[s.switchHtml,'<div id="',n,'" ','style="background:#000;line-height:',p,";height:",p,";width:",h,';color:#fff;text-align:center;">',"\u89c6\u9891\u52a0\u8f7d\u4e2d....<noscript>\u60a8\u7684\u6d4f\u89c8\u5668\u7981\u7528\u4e86JavaScript,\u8bf7\u624b\u52a8\u5f00\u542f.</noscript></div>"].join("")}s.isAndroid&&(s.flashVarsObj.skinNum="-1",s.flashVarsObj.os="android",s.flashVarsObj.oad="",s.flashVarsObj.ead="",s.flashVarsObj.co="2"),typeof s.flashVarsObj["tlogoad"]=="undefined"&&(s.flashVarsObj.tlogoad="http://tv.sohu.com/upload/swf/empty.swf|http://tv.sohu.com/upload/swf/time.swf");try{if(c){var v=n,m=null;typeof v=="string"?m=document.getElementById(v):typeof v=="object"&&(m=v);var g=["<a href='",i?"http://220.181.61.152/fp10_archive/10r18_2/install_flash_player_10_active_x.exe":"http://220.181.61.152/fp10_archive/10r18_2/install_flash_player.exe","' >\u641c\u72d0\u4e0b\u8f7d</a>"].join(""),y="<a href='http://get.adobe.com/flashplayer/' target='_blank' >\u5b98\u65b9\u4e0b\u8f7d</a>",b="\uff0c\u8bf7\u9009\u62e9\u4e0b\u9762\u5730\u5740\u8fdb\u884c\u5b89\u88c5\uff08\u5b89\u88c5\u540e\u9700\u8981\u91cd\u542f\u6d4f\u89c8\u5668\uff09\u5982\u679c\u60a8\u786e\u5b9a\u5df2\u7ecf\u5b89\u88c5\uff0c\u8bf7 <a href='#' rel='play'>\u70b9\u51fb\u8fd9\u91cc\u5c1d\u8bd5\u64ad\u653e</a>",w=["<style>#",v," div{color:#FFF;width:325px;height:118px;padding:10px;background:#262626;border:1px solid #313131;position:absolute;top:50%;left:50%;margin:-64px auto 0 -170px;line-height:1.5em;}","#",v," a{text-decoration:underline;color:#00A2FF;} ","#",v," a:hover{text-decoration:none;color:#00A2FF;}","#",v," p{margin:8px 0;border-top:1px dashed #3C3C3C;border-bottom:1px dashed #3C3C3C;height:34px;line-height:34px;}","</style>"];arHtml=["<div id='_noFlv'>"];var E=s.DetectFlashVer(6,0,65);return r===-1?arHtml.push(["\u60a8\u53ef\u80fd\u6ca1\u6709\u5b89\u88c5FLASH",b,"<p>",g,"\uff08\u63a8\u8350\uff09\u3000\u3000"].join("")):(arHtml.push(["\u60a8\u7684FLASH\u7248\u672c\u4f4e\u4e8e",self.ver.replace(/,/g,"."),b,"<p>"].join("")),E?arHtml.push(["<a rel='update' href='javascript: flvAutoUpdate();'>\u81ea\u52a8\u5347\u7ea7</a>\uff08\u63a8\u8350\uff09\u3000\u3000",g].join("")):arHtml.push([g,"\uff08\u63a8\u8350\uff09"].join(""))),arHtml.push(["\u3000\u3000",y,"</p>\u5b89\u88c5\u5931\u8d25\uff1f<a href='http://tv.sohu.com/upload/hdfeedback/index.jsp?12' target='_blank'>\u70b9\u51fb\u8fd9\u91cc\u67e5\u770b\u89e3\u51b3\u65b9\u6848</a></div>"].join("")),m.innerHTML=[arHtml.join(""),w.join("")].join(""),m.parentNode.style.position="relative",self.update=function(){flvUrl="http://tv.sohu.com/upload/20090903hd/new.swf";var n=document.all?"ActiveX":"PlugIn",r=t.location;document.title=document.title.slice(0,47)+" - Flash Player Installation";var i=document.title,s=new e(flvUrl,"player",so_width,so_height,"6,0,65");s.addParam("FlashVars","MMredirectURL="+r+"&MMplayerType="+n+"&MMdoctitle="+i),s.addParam("wmode","Opaque"),s.addParam("align","middle"),s.addParam("allowscriptaccess","always"),s.addParam("type","application/x-shockwave-flash"),s.addParam("pluginspage","http://www.adobe.com/go/getflashplayer"),document.getElementById(v).innerHTML=s.getFlashHtml()},self.play=function(){var e=new Date;e.setFullYear(e.getFullYear()+1),sohuHDApple.cookie("tryPlay","1",{path:"/",domain:"tv.sohu.com",expires:e}),document.getElementById(v).innerHTML=self.getFlashHtml()},document.getElementById("_noFlv").onclick=function(e){o=e?e:t.event,o=o.target?o.target:o.srcElement,o.tagName=="A"&&o.rel!=""&&(self[o.rel].call(self),e&&e.preventDefault?e.preventDefault():t.event.returnValue=!1)},""}}catch(S){}s.isAndroid||(s.flashVarsObj.topBarFull=1);for(var x in s.flashVarsObj)a.push("&",x,"=",s.flashVarsObj[x]);u.push(s.switchHtml),document.getElementById(s.id)&&(s.id="player"+sohuHDApple.random()),sohuHDApple.playerlist.push(s.id);if(document.all){u.push("<object ");for(var x in s.objAttrs)u.push(x,'="',s.objAttrs[x],'"'," ");u.push(">");for(var x in s.params)u.push('<param name="',x,'" value="',s.params[x],'" />');a.length&&u.push('<param name="flashvars" value="',a.join(""),'" />'),u.push("</object>")}else{u.push("<embed "),s.embedAttrs.FlashVars=a.join("");for(var x in s.embedAttrs)u.push(x,'="',s.embedAttrs[x],'"'," ");u.push("></embed>")}return u.join("")},e.prototype.DetectFlashVer=function(e,t,n){if(r==-1)return!1;if(r!=0){i?(tempArray=r.split(" "),tempString=tempArray[1],versionArray=tempString.split(",")):versionArray=r.split(".");var s=versionArray[0],o=versionArray[1],u=versionArray[2];if(s>parseFloat(e))return!0;if(s==parseFloat(e)){if(o>parseFloat(t))return!0;if(o==parseFloat(t)&&u>=parseFloat(n))return!0}return!1}},e.prototype.checkFlash=function(e){var t=sohuHDApple.cookie("tryPlay");if(t)return!0;var n=this,s=null;typeof e=="string"?s=document.getElementById(e):typeof e=="object"&&(s=e),document.all&&(i=!0);var o=function(){var e="",t="",n="";try{t=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7"),e=t.GetVariable("$version")}catch(n){}if(!e)try{t=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6"),e="WIN 6,0,21,0",t.AllowScriptAccess="always",e=t.GetVariable("$version")}catch(n){}if(!e)try{t=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3"),e=t.GetVariable("$version")}catch(n){}if(!e)try{t=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3"),e="WIN 3,0,18,0"}catch(n){}if(!e)try{t=new ActiveXObject("ShockwaveFlash.ShockwaveFlash"),e="WIN 2,0,0,11"}catch(n){e=-1}return e},u=function(){var e=-1;if(navigator.plugins!=null&&navigator.plugins.length>0){if(navigator.plugins["Shockwave Flash 2.0"]||navigator.plugins["Shockwave Flash"]){var t=navigator.plugins["Shockwave Flash 2.0"]?" 2.0":"",n=navigator.plugins["Shockwave Flash"+t].description,r=n.split(" "),s=r[2].split("."),u=s[0],a=s[1],f=r[3];f==""&&(f=r[4]),f[0]=="d"?f=f.substring(1):f[0]=="r"?(f=f.substring(1),f.indexOf("d")>0&&(f=f.substring(0,f.indexOf("d")))):f[0]=="b"&&(f=f.substring(1));var e=u+"."+a+"."+f}}else navigator.userAgent.toLowerCase().indexOf("webtv/2.6")!=-1?e=4:navigator.userAgent.toLowerCase().indexOf("webtv/2.5")!=-1?e=3:navigator.userAgent.toLowerCase().indexOf("webtv")!=-1?e=2:i&&(e=o());return e},a=n.ver.split(",");r=u();var f=n.DetectFlashVer(a[0],a[1],a[2]);return f?f:f}}(SWFObject,window);

so_width = isWideMod ? 980 : 640;
var _admaster_callback = function (timer, url) {
    var us = [];
    if (window.sohuHD && sohuHD.pingback) {
        us = url.split('|');
        for (var i = 0; i < us.length; i++) {
            if (us[i].indexOf('admaster') > -1) {
                sohuHD.pingback(us[i].replace(/,h,/, ',h' + (new Date()).getTime() + ',') + ',d' + escape(window.location.href));
            } else {
                sohuHD.pingback(us[i]);
            }
        }
    }
};
var _oad_ping_callback =  function (time, url) {
    var pb = sohuHD.pingback;
    if(!pb){
        return;
    }
    var pbs = url.split('|');
    var https = [];
    for(var i=0; i < pbs.length; i++){
        if(pbs[i].search(/\[timestamp\]/) > 0){
            pbs[i] = pbs[i].replace(/\[timestamp\]/, (new Date()).getTime())
        } else {
            https = pbs[i].split(/[^\^]http:\/\//);
            if(https.length > 1){
                pbs[i] = pbs[i] + (https[https.length-1].indexOf('?') > -1 ? '&' : '?') + '_=' + (new Date()).getTime();
            } else if (pbs[i].indexOf('admaster') > -1) {
                pbs[i] = pbs[i].replace(/,h,/,',h'+ (new Date()).getTime() +',') + ',d' + escape(window.location.href);
            } else {
                pbs[i] = pbs[i] + (pbs[i].indexOf('?') > -1 ? '&' : '?') + '_=' + (new Date()).getTime();
            }
        }
        pb(pbs[i]);
    }
    return "1";
};
var so_autoplay = "true";
var so_height = 508;
if (!window.sohuHD) {
    window.sohuHD = {};
}
//2013.12.23:huahua:p2ptest
var _suv = sohuHD.cookie('fuid') || '2';
if (_suv) {
    _suv = parseInt( _suv.substring(_suv.length - 1 ,_suv.length) , 10 );
}

if ( ((vid == 728329 || playlistId == 6520719 || playlistId == 5788506 || playlistId == 6357858 || playlistId == 1010176 || playlistId == 5136748 || playlistId == 6189159 || playlistId == 6357864 || playlistId == 6250606 || playlistId == 5943232 || playlistId == 5773413 || playlistId == 6494217) && /0|1|2|3|4/.test(_suv)) || cid == '16') {
    vrs_player = 'http://tv.sohu.com/upload/swf/p2p/20140424/Main.swf';
}

if ( (playlistId == 6383107 || playlistId == 5025042) && /0|1|2|3|4/.test(_suv) ) {
    vrs_player = 'http://220.181.90.161/webplayer/Main.swf';
}
//end
window.sohuHD.playerUrl = vrs_player;
window.__tv_M && __tv_M.addTag('player_start');
var so = new SWFObject(vrs_player, "player", so_width, so_height, "9,0,115", "#000000");
so.addParam("allowscriptaccess", "always");
so.addParam("allowfullscreen", "true");
so.addParam("wmode", "Opaque");
if (window.isWideMod) {
    so.addVariable("imgCutBtn", "1");
}
if (cid != 9001) {
    so.addVariable("nid", nid);
    so.addVariable("pid", pid);
    so.addVariable("plid", playlistId);
    so.addVariable("pub_catecode", osubcid);
}
so.addVariable("skin", "0");
so.addVariable("domain", "inner");
so.addVariable("cover", cover);
so.addVariable("pageurl", document.URL);
if (cid != '9001' || !_videoInfo || _videoInfo.from == 1) {
    so.addVariable('vid', vid);
} else {
    so.addVariable('id', vid);
}
so.addVariable("sid", sohuHD.cookie("SUV"));
so.addVariable("jump", "0");
so.addVariable("shareBtn", "1");
so.addVariable("cinemaBtn", "1");
so.addVariable("playListId", "1");
so.addVariable("miniWinBtn", "1");
so.addVariable("lightBtn", "1");
so.addVariable("order", window.CatgoryEnum[cid]? window.CatgoryEnum[cid]["order"] : window.CatgoryEnum[0]["order"]);
so.addVariable("onPlayed", "sohuHD.onVideoPlayed");
so.addVariable("onPlay", "sohuHD.onVideoPlay");
so.addVariable('onPlayerReady', 'sohuHD.onPlayerReady');
so.addVariable("onPause", "sohuHD.onVideoPause");
if (window._videoInfo && _videoInfo.vType == '20') {
    so.addVariable("sogouBtn", 0);
}
if (!navigator.userAgent.toLowerCase().match(/version\/([\d.]+).*safari/)) {
    so.addVariable("downloadBtn", "1");
}
if (typeof category != "undefined" && category != "" && cid != 9001) {
    so.addVariable("cmscat", category);
}
if (typeof cid != "undefined" && (cid == "1" || cid == "2")) {
    so.addVariable("isWriteComm", "1");
}
so.addVariable("autoplay", so_autoplay);
//p2ptest
if ( vid == 728329 || playlistId == 1010176 || playlistId == 5025042 || cid == '16') {
    so.addVariable("isSendPID", "1");
}
if (sohuHD.variables) {
    var va = sohuHD.variables;
    for (var i in va) {
        so.addVariable(i, va[i]);
    }
}
so.write('sohuplayer');

messagebus.subscribe('player.update_time', function(topic,  data){window.unload_pingback_url = data.pingback;}, null, null, {cache:true});
window.onbeforeunload = function (e) { e = e || window.event;try{unload_pingback_url&&sohuHD.pingback(unload_pingback_url);} catch (e) {} };

</script>
</div>
        <script>
        messagebus.publish('core.rendervideo');
        </script>
        <!-- Start:left -->
        <div class="left">
           <!-- Start:videoBox -->
            <!--erweima-->
<input type="hidden" id="erwm_list" value="">
<div id="playtoolbar" class="videoBox cfix"></div>
            <!-- End:videoBox -->
      <div class="info-tab">
				<ul class="cfix">
					<li class="s1-tab"><a href="javascript:void(0);" class="s1">信息</a></li>	
					<li class="s2-tab"><a href="javascript:void(0);" class="s2">剧集</a></li>
									
				</ul>
			</div>
        </div>
        <!-- End:left -->
        
        <!-- Start:right -->
        <div class="right">
            <!-- Start:rkBox -->
            <div class="rkBox rkBoxMin cfix">
            </div>
            <!-- End:rkBox -->
        </div>
        <!-- End:right -->
        
    </div>
</div>
<!-- End:playerBar -->
<script>
    messagebus.publish('core.loaded_first_screen');
    </script>
<!-- Start:content -->
<div class="area cfix" id="content">
    <!-- Start:left -->
    <div class="left">
        <!-- Start:info -->
    <div id="playlist">     
      <div class="info info-con">
        <ul class="u cfix">
          
            <li>发布：2014-05-13 18:05
            </li>
            <li class="s">标签：
              <span id="vtags">
              <a href ="javascript:sohuHD.searchKey('火车',null,null);">火车</a> <a href ="javascript:sohuHD.searchKey('亚洲女子天团',null,null);">亚洲女子天团</a> <a href ="javascript:sohuHD.searchKey('飙舞',null,null);">飙舞</a> <a href ="javascript:sohuHD.searchKey('广场舞',null,null);">广场舞</a> 
              </span>
            </li>
            <li class="h">来源：搜狐视频
            </li>
            
            
              <li class="s h">时长：3分10秒
              </li>
            
            <li class="h">类型：<a href ="javascript:sohuHD.searchKey('社会',7,25);">社会</a></li>
             
        </ul>
        <p class="intro">简介：【“亚洲女子天团”火车上飙舞】有网友上传视频，称在K1063车次(兰考—郑州段)火车上，一群大妈在火车上互飙广场舞，气氛很high，炫到不能直视……路人甲大爷在想什么？ 人类已无法阻止广场舞了这种娱乐方式确实罕见，打扑克什么的都弱爆了！。<a href="#" class="info-arrT">展开信息</a></p>
      </div>
      <div id="list"></div>
    </div>
        <!-- End:info -->
        <!-- Start:mod -->
    
      
    
        <!-- End:mod -->
              
      
      <div class="mod mod-list mod-xbtj">
            <div class="mod-tit"><h2>猜你喜欢</h2></div>
            <div class="mod-con">
                <ul class="list list-140 cfix h304" id="similar">                  
                </ul>
<ul class="list list-140 cfix h134" id="myuser">



	 <li class="bwatch" rel="52530044">
		<div class="pic">
			<a class="spic" title="那些被恶搞过的美女辣妹们" href="http://my.tv.sohu.com/us/114999327/52530044.shtml?pvid=cc1c886ccc0050fc" target="_blank">
				<img width="140" height="80" lazysrc="http://i1.itc.cn/20140513/b05_d87a94d8_a451_4eea_7a65_54676d16e0f4_3.jpg" />
			</a>
		</div>
		<strong><a href="http://my.tv.sohu.com/us/114999327/52530044.shtml?pvid=cc1c886ccc0050fc" target="_blank" title="那些被恶搞过的美女辣妹们">那些被恶搞过的美女辣妹们</a></strong>
	</li>


	 <li class="bwatch" rel="68924190">
		<div class="pic">
			<a class="spic" title="女游客和海象合影遭偷袭" href="http://my.tv.sohu.com/us/84369737/68924190.shtml?pvid=cc1c886ccc0050fc" target="_blank">
				<img width="140" height="80" lazysrc="http://i0.itc.cn/20140507/b05_4c43a4b9_d542_7118_d1ef_c49ddb3ab398_1.jpg" />
			</a>
		</div>
		<strong><a href="http://my.tv.sohu.com/us/84369737/68924190.shtml?pvid=cc1c886ccc0050fc" target="_blank" title="女游客和海象合影遭偷袭">女游客和海象合影遭偷袭</a></strong>
	</li>



	<li class="bwatch" rel="69147964">
		<div class="pic">
			<a class="spic" title="盘点那些坑爹的女司机" href="http://my.tv.sohu.com/us/54202377/69147964.shtml?pvid=cc1c886ccc0050fc" target="_blank">
				<img width="140" height="80" lazysrc="http://i1.itc.cn/20140512/b05_40015011_97cb_40fa_b6f7_d7681ea8a188_1.jpg" />
			</a>
		</div>
		<strong><a href="http://my.tv.sohu.com/us/54202377/69147964.shtml?pvid=cc1c886ccc0050fc" target="_blank" title="盘点那些坑爹的女司机">盘点那些坑爹的女司机</a></strong>
	</li>


	<li class="bwatch" rel="68924282">
		<div class="pic">
			<a class="spic" title="情侣间的那些逗比事儿" href="http://my.tv.sohu.com/us/50829474/68924282.shtml?pvid=cc1c886ccc0050fc" target="_blank">
				<img width="140" height="80" lazysrc="http://i0.itc.cn/20140507/b05_4c43a4b9_d542_7118_d1ef_c49ddb3ab398_2.jpg" />
			</a>
		</div>
		<strong><a href="http://my.tv.sohu.com/us/50829474/68924282.shtml?pvid=cc1c886ccc0050fc" target="_blank" title="情侣间的那些逗比事儿">情侣间的那些逗比事儿</a></strong>
	</li>


<li class="bwatch" rel="67693081">
		<div class="pic">
			<a class="spic" title="美女穿紧身裤难免出意外" href="http://my.tv.sohu.com/us/55731236/67693081.shtml?pvid=cc1c886ccc0050fc" target="_blank">
				<img width="140" height="80" lazysrc="http://i3.itc.cn/20140417/b05_284804c2_7940_c322_9075_e2c1ce4f98c2_1.jpg" />
			</a>
		</div>
		<strong><a href="http://my.tv.sohu.com/us/55731236/67693081.shtml?pvid=cc1c886ccc0050fc" target="_blank" title="美女穿紧身裤难免出意外">美女穿紧身裤难免出意外</a></strong>
	</li>







</ul>
            </div>
        </div>
      
      <div class="adv"><div id="cp_100_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_100_1');
</script>
<div class="playad" id="cp_103_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_103_1');
</script>
</div>
      
      <div class="mod mod-list" id="hottv">
            <div class="mod-tit cfix"><h2>卫视同步</h2></div>
            <div class="mod-con">
                <ul class="list list-140 cfix h524">


<li rel="6807767" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140504/n399126473.shtml" title="如果我爱你"><img lazysrc="http://i1.itc.cn/20140507/31fe_411c524c_da71_7d8b_a9eb_f7a9ff60d4e7_1.jpg" width="140" height="190" alt="如果我爱你" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140504/n399126473.shtml" title="如果我爱你">如果我爱你</a></strong> 
                    <p>异域酒庄浪漫情缘</p>
                    </li>

<li rel="5135851" class="awatch">
                   <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140423/n398662724.shtml" title="步步惊情 "><img lazysrc="http://i1.itc.cn/20140423/31fe_8f954081_ca88_bf2c_0842_056ca6684d28_1.jpg" width="140" height="190" alt="步步惊情" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140423/n398662724.shtml" title="步步惊情 ">步步惊情</a></strong> 
                    <p>搜集四爷若曦台词有奖</p>
                    </li>
<li rel="6089908" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140409/n397919777.shtml" title="宫锁连城"><img lazysrc="http://i1.itc.cn/20140410/31fe_44567767_3e70_8bf8_a4d5_6d221d26cc7e_1.jpg" width="140" height="190" alt="宫锁连城" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140409/n397919777.shtml" title="宫锁连城">宫锁连城</a></strong> 
                    <p>于妈很忐忑观众很穿越</p>
 </li>

<li rel="5360914" class="awatch">
                   <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140421/n398595823.shtml" title="金玉良缘 "><img lazysrc="http://i0.itc.cn/20140422/31fe_b38be729_daec_95aa_3649_d52084d9a8ad_1.jpg" width="140" height="190" alt="金玉良缘 " /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140421/n398595823.shtml" title="金玉良缘 ">金玉良缘 </a></strong> 
                    <p>女蛇精病追男记</p>
                    </li>
                   

<li rel="6572871" class="awatch">
                   <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140404/n397793117.shtml" title="我爱男闺蜜"><img lazysrc="http://i2.itc.cn/20140408/31fe_eb25b17e_fcaa_f5e0_9041_87aa99664af3_1.jpg" width="140" height="190" alt="我爱男闺蜜" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140404/n397793117.shtml" title="我爱男闺蜜">我爱男闺蜜</a></strong> 
                    <p>有了男闺蜜 且行且珍惜</p>
                    </li>




<li rel="6787217" class="awatch">
                   <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140423/n398661820.shtml" title="大漠神枪"><img lazysrc="http://i1.itc.cn/20140430/31fe_2f2981ed_568b_ed63_698a_225d9870e501_1.jpg
" width="140" height="190" alt="大漠神枪" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140423/n398661820.shtml" title="大漠神枪">大漠神枪</a></strong> 
                    <p>元芳变牛仔 你怎么看？</p>
                    </li>

<li rel="5773413" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140319/n396889747.shtml" title="一仆二主"><img lazysrc="http://i1.itc.cn/20140321/31fe_687a08c6_7970_4a93_e0df_f1cb68becf1c_1.jpg" width="140" height="190" alt="一仆二主" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140319/n396889747.shtml" title="一仆二主">一仆二主</a></strong> 
                    <p>老少恋姐弟恋不如主仆恋</p>
                    </li>

<li rel="6614209" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140423/n398714190.shtml" title="狙击部队"><img lazysrc="http://i2.itc.cn/20140430/31fe_7d07df71_a50d_22d8_8915_0fedcd8af6a8_1.jpg" width="140" height="190" alt="狙击部队" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140423/n398714190.shtml" title="狙击部队">狙击部队</a></strong> 
                    <p>难得一见“不雷”抗战剧</p>
                    </li>






<li rel="6693023" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140427/n398860621.shtml" title="小宝和老财"><img lazysrc="http://i0.itc.cn/20140430/31fe_c8806c84_1601_8e78_4733_2bc9c5608977_1.jpg
" width="140" height="190" alt="小宝和老财" /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140427/n398860621.shtml" title="小宝和老财">小宝和老财</a></strong> 
                    <p>您且乐着 我给您来一段</p>
                    </li>  
 <li rel="6693013" class="awatch">
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140429/n398996869.shtml" title="薛丁山"><img lazysrc="http://i2.itc.cn/20140507/31fe_49650991_7518_1e7c_490f_d788b7fae14b_1.jpg" width="140" height="190" alt="薛丁山 " /></a><a title="高清" class="super">高清</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140429/n398996869.shtml" title="薛丁山">薛丁山 </a></strong> 
                    <p>一大波隋唐英雄来袭</p>
                    </li>



                </ul>
            </div>
        </div>
    
    
        <div class="adv"><div id="cp_101_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_101_1');
</script>
<div class="playad" id="cp_104_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_104_1');
</script>
</div>
        <!-- Start:mod -->
    
      <div class="mod mod-list" id="vip">
            <div class="mod-tit"><a target="_blank" href="http://tv.sohu.com/vip/?pvid=20bb2041d15215a5" class="btn-vip r">开通会员</a><h2><a target="_blank" href="http://tv.sohu.com/vip/">会员推荐</a>　　 <a target="_blank" href="http://tv.sohu.com/s2014/jay88/index.shtml?pvid=979f6549d8b5fcf2"><font color=red>约会周杰伦，见长腿欧巴！</font></a></h2>
				</div>
            <div class="mod-con">
                <ul class="list list-140 cfix h524">
 <li>                   <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140505/n399167836.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="Q版三国之三小强"><img lazysrc="http://photocdn.sohu.com/20140505/vrsab_ver6810373.jpg" width="140" height="190" alt="Q版三国之三小强" /></a><a title="Q版三国之三小强" class="origin">Q版三国之三小强</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140505/n399167836.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="Q版三国之三小强">Q版三国之三小强</a></strong> 
                    <p>圆眼兄弟爆笑来袭</p>
                    </li>

<li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20131220/n392136704.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="超凡蜘蛛侠"><img lazysrc="http://i2.itc.cn/20140509/872_8f6260ec_10af_e2b3_6a66_015620d139ba_1.jpg" width="140" height="190" alt="超凡蜘蛛侠" /></a><a title="超凡蜘蛛侠" class="origin">超凡蜘蛛侠</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20131220/n392136704.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="超凡蜘蛛侠">超凡蜘蛛侠</a></strong> 
                    <p>蜘蛛侠系列经典延续</p>
                    </li>



  <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140424/n398746733.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="黑帮追缉令"><img lazysrc="http://i1.itc.cn/20140425/872_4cd55b7e_da95_06f3_841a_40e355de7cde_1.jpg" width="140" height="190" alt="黑帮追缉令" /></a> <a title="黑帮追缉令" class="origin">黑帮追缉令</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140424/n398746733.shtml?spayid=301004?pvid=0ce75e6493c7ad43" title="黑帮追缉令">黑帮追缉令</a></strong> 
                    <p>黑帮硬汉卧底复仇</p>
                    </li>     

<li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140418/n398481928.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="我在路上最爱你"><img lazysrc="http://i0.itc.cn/20140419/872_976f6e58_a57f_7c92_1ded_d3793785bbac_1.jpg" width="140" height="190" alt="我在路上最爱你" /></a><a title="我在路上最爱你" class="origin">我在路上最爱你</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140418/n398481928.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="我在路上最爱你">我在路上最爱你</a></strong> 
                    <p>文章啊……哎</p>
   </li>

 <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140416/n398348715.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="菲利普船长 "><img lazysrc="http://i1.itc.cn/20140418/872_b546a75d_daee_4140_0610_ef23b6c21c06_1.jpg" width="140" height="190" alt="菲利普船长 " /></a><a title="菲利普船长 " class="origin">菲利普船长 </a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140416/n398348715.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="菲利普船长 ">菲利普船长 </a></strong> 
                    <p>奥斯卡影帝智斗海盗</p>
                    </li>







                  </li>


<li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20131220/n392134590.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="穿越时空爱上你"><img lazysrc="http://i1.itc.cn/20140429/3137_80a11f61_9cac_af6e_3125_928d30628877_1.jpg" width="140" height="190" alt="穿越时空爱上" /></a><a title="穿越时空爱上你" class="origin">穿越时空爱上你</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20131220/n392134590.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="穿越时空爱上你">穿越时空爱上你</a></strong> 
                    <p>狼叔变身落魄贵族公爵</p>
                    </li>


 <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140328/n397339852.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="西游记之大闹天宫"><img lazysrc="http://i1.itc.cn/20140417/872_5a418f1e_49fb_f4d9_c3ac_cdccecaeb672_1.jpg" width="140" height="190" alt="西游记之大闹天宫" /></a><a title="西游记之大闹天宫" class="origin">西游记之大闹天宫</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140328/n397339852.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="西游记之大闹天宫">西游记之大闹天宫</a></strong> 
                    <p>甄子丹版美猴王恋爱了</p>
                    </li>

 <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20131220/n392131149.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="蜘蛛侠3"><img lazysrc="http://i3.itc.cn/20140505/872_43115e59_8814_df26_ed6d_909b44e09208_1.jpg" width="140" height="190" alt="蜘蛛侠3" /></a><a title="蜘蛛侠3" class="origin">蜘蛛侠3</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20131220/n392131149.shtml?spayid=301004?pvid=0ce75e6493c7ad43" title="蜘蛛侠3">蜘蛛侠3</a></strong> 
                    <p>英雄系列经典之作</p></li>

   <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140504/n399120762.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="机密复仇者：黑寡妇与惩罚者"><img lazysrc="
http://photocdn.sohu.com/20140501/vrsab_ver6810324.jpg" width="140" height="190" alt="机密复仇者：黑寡妇与惩罚者" /></a><a title="机密复仇者：黑寡妇与惩罚者" class="origin">机密复仇者：黑寡妇与惩罚者</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140504/n399120762.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="机密复仇者：黑寡妇与惩罚者">机密复仇者：黑寡妇与惩罚者</a></strong> 
                    <p>复仇最强阵营来袭</p>
                    </li>
 <li>
                    <div class="pic"><a class="apic" target="_blank" href="http://tv.sohu.com/20140504/n399102632.shtml?spayid=301004&pvid=0ce75e6493c7ad43" title="奥斯汀乐园"><img lazysrc="http://photocdn.sohu.com/20140430/vrsab_ver6810314.jpg" width="140" height="190" alt="奥斯汀乐园" /></a><a title="奥斯汀乐园" class="origin">奥斯汀乐园</a> </div>
                    <strong><a target="_blank" href="http://tv.sohu.com/20140504/n399102632.shtml?spavid=301004?pvid=0ce75e6493c7ad43" title="奥斯汀乐园">奥斯汀乐园</a></strong> 
                    <p>达西情结少女疯狂追爱</p>
                    </li>

   



     


























 







 




    

 


 


  


         





                 





                </ul>
            </div>
        </div>
    
     <!-- End:mod -->
    </div>
    <!-- End:left -->
  <script>
        messagebus.publish('core.loaded_left');
        </script>
    <!-- Start:right -->
    <div class="right">
        <!-- Start:remark -->
        <div class="remark">
        <p class="remark-count cfix" style="display:none;"><span class="l">共 <a id="commTotal" title="全部评论" class="rc entry" target="_blank" href="#">0</a> 条评论</span>
            <a href="#" class="r fs12 entry" title="全部评论" target="_blank">全部评论</a>
        </p>
        <div id="commList">    </div> 
        <div class="rTotal cfix" id="commPage">
            <a class="entry l fs12" href="#" title="全部评论" target="_blank" style="display:none;">查看全部评论</a>
            <div id="pagination_5" class=" pages-1 r"></div>    
        </div>
    </div>

    <!-- End:remark -->
        <div class="adv mB20"><div id="cp_102_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('cp_102_1');
</script></div>
        <!-- Start:charts -->
    
      

      <div class="rank" id="usershare">
    <div class="title cfix"><h2>用户分享</h2>
    </div>
    <div class="mod-con">
        <ul class="list listA cfix">
            

            <li class="cfix bwatch" rel="69070238">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/50333101/69070238.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i3.itc.cn/20140512/31f2_2d660440_ba94_00d0_56c3_b224b7164d4b_1.jpg" alt="爱贴喵星人冷屁股的汪星人" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/50333101/69070238.shtml?pvid=fe6789abda895e1f">爱贴喵星人冷屁股的汪星人</a></strong>
            </li>

            <li class="cfix bwatch" rel="68116829">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/194315962/68116829.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i2.itc.cn/20140425/31f2_c13e3b67_8471_505b_7643_06f7a5d5c109_1.jpg" alt="男子收集高校女生千余文胸" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/194315962/68116829.shtml?pvid=fe6789abda895e1f">男子收集高校女生千余文胸</a></strong>
            </li>

            <li class="cfix bwatch" rel="68890171">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/201150369/68890171.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i0.itc.cn/20140508/31f2_ead662e3_5b31_d215_7872_8ae1383e7880_1.jpg" alt="那些在孩子面前出糗的水爹们" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/201150369/68890171.shtml?pvid=fe6789abda895e1f">那些在孩子面前出糗的水爹们</a></strong>
            </li>

            <li class="cfix bwatch" rel="68749376">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/18238496/68749376.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i0.itc.cn/20140505/31f2_c68fe628_4f19_1f2e_73f6_c97167b66087_1.jpg" alt="CCXV强剧寨见谢耳朵" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/18238496/68749376.shtml?pvid=fe6789abda895e1f">CCXV强剧寨见谢耳朵</a></strong>
            </li>

            <li class="cfix bwatch" rel="69148724">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/201150369/69148724.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i1.itc.cn/20140513/31f2_3d60601e_33f2_74bf_8732_c1416fc84b4c_1.jpg" alt="听说妹子们自拍喜欢嘟嘟嘴" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/201150369/69148724.shtml?pvid=fe6789abda895e1f">听说妹子们自拍喜欢嘟嘟嘴</a></strong>
            </li>

            <li class="cfix bwatch" rel="68951413">
            <div class="pic">
                <a target="_blank" href="http://my.tv.sohu.com/us/201839278/68951413.shtml?pvid=fe6789abda895e1f"><img width="88" height="88" lazySrc="http://i3.itc.cn/20140509/31f2_f5605050_71b7_8361_7cbd_cc5bd37d4716_1.jpg" alt="迪拜土豪奢华游艇欢迎跪拜" class="sz6"></a>
            </div>
            <strong><a target="_blank" href="http://my.tv.sohu.com/us/201839278/68951413.shtml?pvid=fe6789abda895e1f">迪拜土豪奢华游艇欢迎跪拜</a></strong>
            </li>

        </ul>
    </div>
</div>
    

        <!-- End:charts -->
        <div class="adv"><div id="rec_100_1"></div>
<script type="text/javascript">
       _sohuHD.AD.init('rec_100_1');
</script></div>
    </div>
    <!-- End:right -->
  <script>
        messagebus.publish('core.loaded_right');
        </script>
</div>
<!-- End:content -->
<div class="sbtn-wrap" pb-url="pg_playbang">
	<span class="sbtn-rank">榜</span>
	<!-- Start:rankBox -->
	<div class="rankBox">
		<div class="mod-tit">
			<h4>热门排行</h4>
			<a class="top50" href="#" target="_blank">TOP50>></a>
		</div>
		<div class="rTab_con cfix">
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140513/n399467651.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140505/vrsab_ver6810369.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">1</i>产科男医生</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">1</i><em class="e1">产科男医生</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/27768" target="_blank">李小璐</a>
																																																																																																								                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																1,707万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140512/n399467621.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140429/vrsab_ver6807767.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">2</i>如果我爱你</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">2</i><em class="e1">如果我爱你</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/312694" target="_blank">明道</a>
																																																																																											                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																1,005万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20140423/n398662724.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140417/vrsab_ver5135851.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">3</i>步步惊情</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">3</i><em class="e1">步步惊情</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/274475" target="_blank">刘诗诗</a>
																																																																														                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																991万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140421/n398595823.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20130516/vrsab_ver5360914.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">4</i>金玉良缘</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">4</i><em class="e1">金玉良缘</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/15711" target="_blank">霍建华</a>
																																																																														                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																458万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140423/n398714190.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140423/vrsab_ver6804702.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">5</i>狙击部队</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">5</i><em class="e1">狙击部队</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/316331" target="_blank">王珂</a>
																																																																																											                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																451万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
				            <a href="http://tv.sohu.com/20140512/n399467259.shtml?fid=514&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140417/vrsab_ver6693023.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">6</i>小宝和老财</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">6</i><em class="e1">小宝和老财</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/51520" target="_blank">范伟</a>
																																																																																											                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																448万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
	
</div>
		<div class="rTab_con cfix">
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140512/n399446325.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140421/vrsab_ver6787218.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">1</i>蛇蝎女佣第2季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">1</i><em class="e1">蛇蝎女佣第2季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/68" target="_blank">罗塞莉·桑切斯</a>
																																																																	                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																81万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20130924/n387126789.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20130807/vrsab_ver5690705.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">2</i>破产姐妹第3季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">2</i><em class="e1">破产姐妹第3季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/18974" target="_blank">凯特·戴琳斯</a>
																																																				                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																57万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140508/n399295737.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20130814/vrsab_ver5703605.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">3</i>绿箭侠第2季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">3</i><em class="e1">绿箭侠第2季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/17933" target="_blank">薇拉·贺兰德</a>
																																							                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																38万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140214/n395013286.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140207/vrsab_ver6279221.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">4</i>纸牌屋第2季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">4</i><em class="e1">纸牌屋第2季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/54426" target="_blank">凯文·史派西</a>
																																																				                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																34万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
				            <a href="http://tv.sohu.com/20140507/n399248243.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20130711/vrsab_ver5590402.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">5</i>神盾局特工第1季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">5</i><em class="e1">神盾局特工第1季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/84" target="_blank">克拉克·格雷格</a>
																																																																	                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																28万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20130914/n386591910.shtml?fid=515&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20130815/vrsab_ver5703631.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">6</i>越狱第1季</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">6</i><em class="e1">越狱第1季</em></span>
						                    <span class="cfix"><i class="i2">主演：</i>
					<em class="e2">
													                                <a href="http://so.tv.sohu.com/star/41024" target="_blank">温特沃斯·米勒</a>
																																							                    </em>
				</span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																27万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
	
</div>
		<div class="rTab_con cfix">
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20140509/n399360439.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140424/vrsab_ver6806007.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">1</i>林中女妖</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">1</i><em class="e1">林中女妖</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																29万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20130515/n376037733.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20130515/vrsab_ver5360218.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">2</i>我的P.S.搭档</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">2</i><em class="e1">我的P.S.搭档</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																27万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20120730/n349397234.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20120710/vrsab_ver5025042.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">3</i>两个女人</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">3</i><em class="e1">两个女人</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																26万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140507/n399264441.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140428/vrsab_ver1012797.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">4</i>如沐爱河</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">4</i><em class="e1">如沐爱河</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																25万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140428/n398940672.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140328/vrsab_ver5259664.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">5</i>饥饿游戏2：星火燎原</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">5</i><em class="e1">饥饿游戏2：星火燎原</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																25万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20140410/n398053068.shtml?fid=518&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20140109/vrsab_ver6383107.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">6</i>大话天仙</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">6</i><em class="e1">大话天仙</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																21万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
	
</div>
		<div class="rTab_con cfix">
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140511/n399404276.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20130624/vrsab_ver1007474.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">1</i>航海王</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">1</i><em class="e1">航海王</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																770万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
				            <a href="http://tv.sohu.com/20140510/n399387356.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140404/vrsab_ver1007177.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">2</i>妖精的尾巴</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">2</i><em class="e1">妖精的尾巴</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																145万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta pic_meta_red">
								<a href="http://tv.sohu.com/20130423/n373706861.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20130626/vrsab_ver5269311.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">3</i>七龙珠Z</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">3</i><em class="e1">七龙珠Z</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																102万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
								<a href="http://tv.sohu.com/20131221/n392169750.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
					<img src="http://photocdn.sohu.com/20131227/vrsab_ver6279208.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">4</i>猪猪侠之变身小英雄</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">4</i><em class="e1">猪猪侠之变身小英雄</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																72万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
				            <a href="http://tv.sohu.com/20140414/n398224779.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20140103/vrsab_ver6357809.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">5</i>贝瓦儿歌</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">5</i><em class="e1">贝瓦儿歌</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																70万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
			<!-- Start:pic_meta-->
		        	<div class="pic_meta">
				            <a href="http://tv.sohu.com/20140221/n395444915.shtml?fid=556&pvid=4d4db6d26aa0a4ec" class="pic" target="_blank">
        			<img src="http://photocdn.sohu.com/20121031/vrsab_ver5102665.jpg" width="100" height="135" alt="图片" />
		</a>

		<div class="default">
			<span class="maskBg"></span>
			<span class="maskTx"><i class="i1">6</i>名侦探柯南（国语）</span>
		</div>

		<div class="over">
			<span class="maskBg"></span>
			<div class="maskTx">
				<span class="cfix"><i class="i1">6</i><em class="e1">名侦探柯南（国语）</em></span>
				
				<span class="cfix"><i class="i2">播放：</i>
				<em class="e2">
																69万
									</em>
				</span>

			</div>
		</div>
		</div>
		<!-- End:pic_meta -->
	
</div>
		<ul class="rTab_menu cfix">
			<li data-link="http://tv.sohu.com/hotdrama/"><a>电视剧</a></li>
			<li data-link="http://tv.sohu.com/rank/usa_tv.shtml"><a>美剧</a></li>			
			<li data-link="http://tv.sohu.com/hotmovie/"><a>电影</a></li>
			<li data-link="http://tv.sohu.com/hotcomic/"><a>动漫</a></li>
		</ul>
	</div>
	<!-- End:rankBox -->
</div>
<!-- Start:footer -->
<div id="footArea">
    <div class="footSearch">
        <div class="search">
            <form id="sFormA" autocomplete="off" target="_blank" onSubmit="return false;" name="sFormA" method="post">
                <div class="text l" onMouseOut="this.className='text l'" onMouseDown="this.className='text_click l'"><input type="text" id="sKeyA" class="fs14" value="隐秘而伟大"></div>
                <input type="submit" class="bt vat pointer l" value="" onMouseOut="this.className='bt vat pointer l'" onMouseDown="this.className='btDown vat pointer l'" onMouseOver="this.className='btOver vat pointer l'">
            </form>
        </div>
    </div>
    <div class="clear footLink">
        <dl>
            <dt><a href="http://tv.sohu.com/" target="_blank">首页</a></dt>
            <dd><a target="_blank" href="http://tv.sohu.com/drama/">电视剧</a><a href="http://tv.sohu.com/movie/" target="_blank">电影</a><br><a href="http://tv.sohu.com/documentary/" target="_blank">纪录片</a><a href="http://tv.sohu.com/comic/" target="_blank">动漫</a></dd>
        </dl>
        <dl>
            <dt><a href="http://tv.sohu.com/yule/" target="_blank">娱乐</a></dt>
            <dd><a href="http://tv.sohu.com/self/" target="_blank">搜狐出品</a><a href="http://tv.sohu.com/music/" target="_blank">音乐</a><br><a href="http://tv.sohu.com/show/" target="_blank">综艺</a><a href="http://tv.sohu.com/entnews/" target="_blank">娱乐新闻</a><br><a href="http://tv.sohu.com/microprogram/" target="_blank">微栏目</a></dd>
        </dl>
        <dl>
            <dt><a href="http://tv.sohu.com/news/" target="_blank">新闻</a></dt>
            <dd><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u56fd_u5185_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">国内</a><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u56fd_u9645_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">国际</a><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u519b_u4e8b_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">军事</a><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u79d1_u6280_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">科技</a><br><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u8d22_u7ecf_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">财经</a><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u793e_u4f1a_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">社会</a><a target="_blank" href="http://so.tv.sohu.com/list_p11300_p2_u751f_u6d3b_u89c6_u89d2_p3_p4-1_p5_p6_p73_p80_p9-2_p101_p11.html">生活</a><a target="_blank" href="http://tv.sohu.com/travel/">旅游</a></dd>
        </dl>
        <dl>
            <dt><a href="http://tv.sohu.com/drama/" target="_blank">电视</a></dt>
            <dd><a href="http://tv.sohu.com/live/" target="_blank">直播</a><br><a href="http://live.tv.sohu.com/jmyg" target="_blank">节目</a></dd>
        </dl>
        <dl>
            <dt><a href="http://my.tv.sohu.com/" target="_blank">空间</a></dt>
            <dd><a target="_blank" href="http://my.tv.sohu.com/user/cc133">搞笑</a><a target="_blank" href="http://tv.sohu.com/game/">游戏</a><br><a target="_blank" href="http://my.tv.sohu.com/user/cc124">原创</a><a target="_blank" href="http://my.tv.sohu.com/user/cc112">娱乐</a></dd>
        </dl>
        <dl>
            <dt><a href="http://tv.sohu.com/vip/" target="_blank">会员</a></dt>
            <dd><a href="http://tv.sohu.com/vip/" target="_blank">电影</a><a href="http://tv.sohu.com/edu/" target="_blank">教育</a><br><a href="http://tv.sohu.com/vip/" target="_blank">去广告</a></dd>
        </dl>
        <div class="did_line"></div>
        <dl>
            <dt><a>服务</a></dt>
            <dd>
				<a target="_blank" href="http://lm.tv.sohu.com">网站联盟</a>
				<a target="_blank" href="http://open.tv.sohu.com">开放平台</a>
				<br>
                <a class="a5ico" target="_blank" href="http://help.tv.sohu.com/list.do?id=35">版权投诉</a>
				<a class="a4" target="_blank" href="http://tv.sohu.com/about/">关于我们</a>
				<br>
                <a class="a1" target="_blank" href="http://index.tv.sohu.com/">指数</a>
                <a target="_blank" href="http://tv.sohu.com/upload/feedback/feedback.html">反馈</a>
                <a target="_blank" href="http://help.tv.sohu.com/index.do">帮助</a>                
            </dd>
        </dl>
        <dl>
            <dt><a>软件</a></dt>
            <dd class="lastdd"><a href="http://tv.sohu.com/sohuapp" target="_blank" class="a2">移动客户端</a><br><a href="http://tv.sohu.com/app" target="_blank" class="a3">搜狐影音</a>
<br><a href="http://my.tv.sohu.com/user/video/cloudreg.do#regContainer" target="_blank" class="a3">云剪辑</a></dd>
        </dl>
    </div>
</div>
<div id="foot"> 
    <div class="area tac"> <a href="javascript:void(0)" onClick="this.style.behavior='url(#default#homepage)';this.setHomePage('http://www.sohu.com');return false;">设置首页</a> - <a href="http://pinyin.sogou.com/" target="_blank">搜狗输入法</a> - <a href="http://pay.sohu.com/payment/index.action" rel=nofollow target="_blank">支付中心</a> - <a href="http://hr.sohu.com" target="_blank">搜狐招聘</a> - <a href="http://ad.sohu.com/" rel=nofollow target="_blank">广告服务</a> - <a href="http://sohucallcenter.blog.sohu.com/" rel=nofollow target="_blank">客服中心</a> - <a href="http://corp.sohu.com/s2006/contactus/" rel=nofollow target="_blank">联系方式</a> - <a href="http://www.sohu.com/about/privacy.html" rel=nofollow target="_blank">保护隐私权</a> - <a href="http://corp.sohu.com/" rel=nofollow target="_blank">About SOHU</a> - <a href="http://corp.sohu.com/indexcn.shtml" rel=nofollow target="_blank">公司介绍</a> <br>Copyright <span class="fontArial">&copy;</span> <script>document.write(new Date().getFullYear());</script> Sohu.com Inc. All Rights Reserved. 飞狐信息技术(天津)有限公司 <span class="unline"><a href="http://corp.sohu.com/s2007/copyright/" target="_blank">版权所有</a></span> <br>搜狐不良信息举报电话：010－62728061 举报邮箱：<a href="mailto:jubao@contact.sohu.com">jubao@contact.sohu.com</a> </div> 
</div>
<!-- End:footer -->
<script>
window.__tv_M && __tv_M.addTag('foot');
messagebus.publish('core.loaded_end');
</script>
<script>
messagebus.publish('play.loaded_manual_similar_data', [
{
    playlistId: 6810354,
    videoBigPic: "http://i3.itc.cn/20140509/2b8a_6988e3f2_fb96_513a_eb61_2c39e73f2586_1.jpg",
    videoName: "24小时",
    videoUrl: "http://tv.sohu.com/20140506/n399197843.shtml"
},
{
    playlistId: 6810369,
    videoBigPic: "http://i3.itc.cn/20140512/2b8a_2980a265_1831_d867_e19e_7b56daf89cad_1.jpg",
    videoName: "产科男医生",
    videoUrl: "http://tv.sohu.com/20140508/n399271607.shtml"
}]);
</script>

<script>
var _iwt_UA="UA-sohu-123456";
</script>
<script type="text/javascript" src="http://tv.sohu.com/upload/Trace/iwt-min.js"></script>
<script type="text/javascript" src="http://js.tv.itc.cn/hdpv.js"></script>
<!-- Begin comScore Tag --> 
<script> 
  document.write(unescape("%3Cscript src=' " + (document.location.protocol == "https:" ? "https://sb" : "http://b") 
+ ".scorecardresearch.com/beacon.js'  %3E%3C/script%3E")); 

</script> 
 
<script> 
if(typeof COMSCORE!=="undefined"){
  COMSCORE.beacon({ 
    c1:2, 
    c2:"7395122", 
    c3:"", 
    c4:"", 
    c5:"", 
    c6:"", 
    c15:"" 
  }); 
}
</script> 
<noscript> 
  <img src="http://b.scorecardresearch.com/p?c1=2&c2=7395122&c3=&c4=&c5=&c6=&c15=&cj=1" /> 
</noscript> 
<!-- End comScore Tag -->
<script type="text/javascript" language="javascript" src="http://a1.itc.cn/pv/js/spv.1305141919.js"></script>
<!-- START WRating v1.0 -->
<script type="text/javascript" src="http://tv.sohu.com/upload/Trace/wrating.js"></script>
<script type="text/javascript">
var vjAcc="860010-2288050100";
var wrUrl="http://sohu.wrating.com/";
vjTrack("");
</script>
<noscript><img src="http://sohu.wrating.com/a.gif?a=&c=860010-2288050100" width="1" height="1"/></noscript>

<!-- END WRating v1.0 -->



</body>
</html>


"""
pipe = Pipelines(content)
pipe.process()






