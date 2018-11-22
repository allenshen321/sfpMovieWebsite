$(document).ready(function () {

    let site_map = [];  // 存放电影资源信息


    //右边资源类型

    /*
    $("#content div.aside").prepend(`<div id="drdm_req_status" style="color: #C65E24;background: #F4F4EC; padding: 10px; margin-bottom: 20px; word-wrap: break-word;">
    <div style="text-align: center;">资源搜索情况 <a href="javascript:void();" id="drdm_req_status_hide">(隐藏)</a> <hr></div>
    <p id="drdm_dep_notice" style="color: #C65E24;">脚本未完全加载，部分站点将受影响。请确保网络稳定或尝试重新刷新页面。</p>
    <table>
    <tr><td width="50%">存在：<span id="drdm_req_success"></span></td><td width="50%">不存在：<span id="drdm_req_noexist"></span></td></tr>
    <tr><td width="50%">请求中：<span id="drdm_req_asking"></span></td><td width="50%">失败或需要登陆：<span id="drdm_req_fail"></span></td></tr>
    </table>
    <span id="drdm_req_help"><hr>
    <span>是否隐藏当前未成功的搜索项？  <a href="javascript:void();" id="drdm_hide_fail"> 是 </a>  /  <a href="javascript:void();" id="drdm_show_all"> 否 </a></span>
    </span>
    </div>
    
    <div id='adv-sites'></div>`);

    $("#drdm_req_status_hide").click(function () {
        $("#drdm_req_status").hide();
    });
    $("#drdm_hide_fail").click(function () {
        $("#adv-sites a[title!=\"资源存在\"]").hide();
    });
    $("#drdm_show_all").click(function () {
        $("#adv-sites a:hidden").show();
    });
    */
    $('#content div.aside').prepend('<h3>电影资源搜索：</h3><div id="adv-sites"></div>')

    let update_status_interval;

    function update_req_status() {
        let asking_length = $("#adv-sites a[title=\"正在请求信息中\"]").length;

        $("#drdm_req_success").text($("#adv-sites a[title=\"资源存在\"]").length);
        $("#drdm_req_asking").text(asking_length);
        $("#drdm_req_noexist").text($("#adv-sites a[title=\"资源不存在\"]").length);
        $("#drdm_req_fail").text($("#adv-sites a[title=\"站点需要登陆\"]").length + $("#adv-sites a[title=\"遇到问题\"]").length);

        if (asking_length === 0) {
            clearInterval(update_status_interval);
        } // 当所有请求完成后清除定时器
    }

    function _encodeToGb2312(str, opt) {
        let ret = "";
        try {
            ret = encodeToGb2312(str, opt);
        } catch (e) {
            ret = Math.random() * 1e6;
            $("#drdm_dep_notice").show();
        }
        return ret;
    }

    // 获取电影名
    let unititle = $('#movie-name h1').text();

    // 判断是否是动漫
    let is_anime = false;





    site_map.push({
        name: "在线正版影视",
        label: [
            { name: '爱奇艺视频', link: 'https://so.iqiyi.com/so/q_' + unititle, selector: "div.mod_result span.play_source" },
            { name: '哔哩哔哩', link: 'https://search.bilibili.com/all?keyword=' + unititle, selector: 'div.info-items div.top-info' },
            { name: '乐视视频', link: 'http://so.le.com/s?wd=' + unititle, selector: `h1 > a.j-baidu-a[title*='${unititle}']` },
            { name: '芒果TV', link: 'https://so.mgtv.com/so/k-' + unititle, selector: 'div.so-result-info.clearfix span.label' },
            { name: '搜狐视频', link: 'https://so.tv.sohu.com/mts?wd=' + unititle, selector: 'div.wrap.cfix div.cfix.resource' },
            { name: '腾讯视频', link: 'https://v.qq.com/x/search/?q=' + unititle, selector: 'div.wrapper_main div._infos' },
            { name: '优酷视频', link: 'https://www.soku.com/nt/search/q_' + unititle, selector: 'div.s_intr span.intr_area.c_main' },
        ]
    });

    site_map.push({
        name: "在线影视视频",
        label: [
            { name: '4K屋', link: 'http://www.4kwu.cc/?m=vod-search&wd=' + unititle, selector: 'div.tv-bd.search-list div.item_txt' },
            { name: 'AAQQS', link: 'http://aaxxy.com/vod-search-pg-1-wd-' + unititle + '.html', selector: '#find-focus li' },
            { name: 'Neets', link: 'http://neets.cc/search?key=' + unititle, selector: '#search_li_box div.search_li.clearfix' },
            { name: 'Q2电影网', link: 'http://www.q2002.com/search?wd=' + unititle, selector: 'div.container div.movie-item' },
            { name: '霸气村', link: 'http://www.baqicun.co/search.php?searchword=' + unititle, selector: 'div.k_sou div.k_sou-4' },
            { name: '电影盒子', method: "post", link: 'http://www.5iwanyouxi.com/index.php?s=vod-search-name&wd=' + unititle, data: `wd=${unititle}`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: 'div.v_tb div.v_txt' },
            { name: '嗨哆咪影视', link: 'http://www.haiduomi.com/search.html?wd=' + unititle, selector: 'div.theiaStickySidebar h1.fed-part-eone.fed-font-xvi' },
            { name: '魔力电影网', link: 'http://www.magbt.net/search.php?searchword=' + unititle, selector: '#content li.listfl' },
            { name: '新论语', link: 'http://www.honggujiu.com/index.php?m=vod-search&wd=' + unititle, selector: 'div.col-xs-12 div.meta' },
            { name: '左手吃斋', link: 'https://www.zsczys.com/index.php?m=vod-search&wd=' + unititle, selector: 'div.col-xs-12 div.meta' },
        ]
    });

    site_map.push({
        name: "电影资源下载",
        label: [
            { name: '2TU影院', link: 'http://www.82tu.cc/search.php?submit=%E6%90%9C+%E7%B4%A2&searchword=' + unititle, selector: 'ul.mlist div.info' },
            { name: '4K电影', link: 'https://www.dygc.org/?s=' + unititle, selector: 'div.mi_cont h3.dytit' },
            { name: '52 Movie', link: 'http://www.52movieba.com/search.htm?keyword=' + unititle, selector: 'table.table.table-hover.threadlist tr.thread.tap' },
            { name: '592美剧', link: 'http://www.592meiju.com/search/?wd=' + unititle, selector: 'ul.serach-ul div.info' },
            // { name: '66影视网', method: "post", link: 'https://www.66ys.tv/e/search/index.php', data: `show=title%2Csmalltext&tempid=1&tbname=Article&keyboard=${gunititle}&Submit22=%E6%90%9C%E7%B4%A2`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: "div.listBox li" },
            // { name: '6V电影网', method: "post", link: 'http://www.6vhao.tv/e/search/index.php', data: `show=title%2Csmalltext&tempid=1&tbname=Article&keyboard=${gunititle}&Submit22=%E6%90%9C%E7%B4%A2`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: "div.listBox li" },
            // { name: '8V电影网', link: 'http://www.8vdy.com/search.asp?searchword=' + gunititle, selector: '#div_2 div.listInfo' },
            { name: '80s手机', method: "post", link: 'https://www.80s.tw/search#search_' + unititle, data: `keyword=${unititle}`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, selector: '#block3 i.fa.fa-film' },
            // { name: '962电影网', link: 'http://www.fx962.com/search.asp?searchword=' + gunititle, selector: '#contents li' },
            { name: '97电影网', link: 'http://www.id97.com/search?q=' + unititle, selector: 'div.container div.col-xs-7' },
            { name: '98TVS', link: 'http://www.98tvs.com/?s=' + unititle, selector: '#post_container li' },
            { name: '9去这里', link: 'http://9qzl.com/index.php?s=/video/search/wd/' + unititle, selector: "ul.mov_list li" },
            { name: 'CK电影', link: 'http://www.ck180.net/search.html?q=' + unititle, selector: 'ul.serach-ul div.info' },
            { name: 'LOL电影', link: 'http://www.993dy.com/index.php?m=vod-search&wd=' + unititle, selector: 'div.movielist a.play-img' },
            { name: 'MP4Vv', link: 'http://www.mp4pa.com/search.php?searchword=' + unititle, selector: 'ul.list-unstyled h4.weixin' },
            { name: 'MP4电影', link: 'http://www.domp4.com/search/' + unititle + '-1.html', selector: 'div.vodlist_l.box div.play_info' },
            // { name: 'TKing', link: 'https://torrentking.eu/search?mk=' + eng_title, selector: '#slider-runningshows div.slide-item' },
            { name: 'TL95', link: 'http://www.tl95.com/?s=' + unititle, selector: `li.entry-title > a:contains(${unititle})` },
            { name: '爱下电影网', link: 'http://www.aixia.cc/plus/search.php?searchtype=titlekeyword&q=' + unititle, selector: 'div.con li' },
            { name: '比特大雄', link: 'https://www.btdx8.com/?s=' + unititle, selector: '#content div.post.clearfix' },
            { name: '比特影视', link: 'https://www.bteye.com/search/' + unititle, selector: '#main div.item' },
            { name: '创世影院', link: 'http://www.cuangs.com/so/' + unititle, selector: 'div.box span' },
            { name: '第一电影网', link: 'https://www.001d.com/?s=' + unititle, selector: 'div.mainleft div.info' },
            // { name: '电影港', method: "post", link: 'http://so.dygang.net/e/search/index.php', data: `tempid=1&tbname=article&keyboard=${gunititle}&show=title%2Csmalltext&Submit=%CB%D1%CB%F7`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: "table[width='100%'][border='0'][cellspacing='0'][cellpadding='0'] a.classlinkclass" },
            { name: '电影日志', link: 'http://www.dyrizhi.com/search?s=' + unititle, selector: 'div.pure-g div.item' },
            { name: '电影首发站', link: 'http://www.dysfz.vip/key/' + unititle + '/', selector: '.movie-list li' },
            // { name: '电影天堂', method: "post", link: 'https://www.dy2018.com/e/search/index.php', data: `show=title%2Csmalltext&tempid=1&keyboard=${gunititle}&Submit=%C1%A2%BC%B4%CB%D1%CB%F7`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: 'div.co_content8 table' },
            { name: '钉子电影', method: "post", link: 'http://www.dingzibd.com/q#search_' + unititle, data: `keyword=${unititle}`, csrf: { name: "_csrf", update: "data" }, headers: { "Content-Type": "application/x-www-form-urlencoded" }, selector: `h4 > a:contains(${unititle})` },
            { name: '嘎嘎影视', link: 'http://www.gagays.xyz/movie/search?req%5Bkw%5D=' + unititle, selector: '#movie-sub-cont-db div.large-movie-detail' },
            { name: '高清888', link: 'https://www.gaoqing888.com/search?kw=' + unititle, selector: 'div.wp-content div.video-row' },
            { name: '高清MP4', link: 'http://www.mp4ba.com/index.php?m=vod-search&wd=' + unititle, selector: '#data_list tr.alt1' },
            { name: '高清电台', link: 'https://gaoqing.fm/s.php?q=' + unititle, selector: '#result1 div.row' },
            { name: '高清控', link: 'http://www.gaoqingkong.com/?s=' + unititle, selector: '#post_container div.post_hover' },
            { name: '户户盘', method: "post", link: 'http://huhupan.com/e/search/index.php', data: `keyboard=${unititle}&show=title&tempid=1&tbname=news&mid=1&depost=search`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: 'div.main h2' },
            { name: '界绍部', link: 'http://www.jsb456.com/?s=' + unititle, selector: '#content h2.title' },
            { name: '就爱那片', method: "post", link: 'http://www.inapian.com/index.php?s=vod-search&wd=' + unititle, data: `wd=${unititle}`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: 'div.sortcon div.minfo' },
            { name: '看美剧', link: 'http://www.kanmeiju.net/index.php?s=/video/search/wd/' + unititle, selector: 'div.listri p.t' },
            { name: '蓝光网', link: 'http://www.languang.co/?s=' + unititle, selector: 'div.mi_cont li' },
            { name: '老司机电影', link: 'http://www.lsjdyw.net/search/?s=' + unititle, selector: 'div.row div.row.list.shadow' },
            { name: "乐赏电影", link: 'http://www.gscq.me/search.htm?keyword=' + unititle, selector: 'div.media-body div.subject.break-all' },
            { name: '美剧仓库', method: "post", link: 'http://www.meijuck.com/e/search/index.php', data: `show=title&tempid=1&tbname=news&mid=1&dopost=search&keyboard=${unititle}&submit=`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: "div.content-wrap p.note" },
            { name: "美剧汇", link: 'http://www.meijuhui.net/search.php?q=' + unititle, selector: 'article.excerpt li.focus' },
            { name: '美剧鸟', link: 'http://www.meijuniao.com/index.php?s=vod-search-wd-' + unititle + '.html', headers: { "X-Requested-With": "XMLHttpRequest" }, ajax: "http://www.meijuniao.com/index.php?s=vod-search-wd-" + unititle + "-1-ajax", type: "json", selector: 'data.count > 0' },
            { name: '迷你MP4', link: 'http://www.minimp4.com/search?q=' + unititle, selector: 'div.container div.col-xs-7' },
            { name: '泡饭影视', link: 'http://www.chapaofan.com/search/' + unititle, selector: `li a[title*='${unititle}']` },
            { name: '片吧', link: 'http://so.pianbar.com/search.aspx?q=' + unititle, selector: `h4.media-heading + span:contains(${unititle})` },
            { name: '片源网', link: 'http://pianyuan.net/search?q=' + unititle, selector: 'div.row ul.detail' },
            { name: '飘花资源网', link: 'https://www.piaohua.com/plus/search.php?kwtype=0&keyword=' + unititle, selector: 'div.container div.txt' },
            { name: '趣味源', link: 'http://quweiyuan.cc/?s=' + unititle, selector: `h2.post-entry-headline a:contains(${unititle})` },
            { name: '人生05', link: 'http://www.rs05.com/search.php?s=' + unititle, selector: '#movielist li' },
            { name: '贪玩影视', link: 'http://www.tanwanyingshi.com/movie/search?keyword=' + unititle, selector: 'div.col-md-8 div.service-content' },
            { name: '新6V电影', method: "post", link: 'https://www.66s.cc/e/search/index.php', data: `show=title&tempid=1&tbname=article&mid=1&dopost=search&submit=&keyboard=${unititle}`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: '#post_container div.entry_post' },
            { name: '新片网', link: 'http://www.91xinpian.com/index.php?m=vod-search&wd=' + unititle, selector: 'div.search span.name' },
            { name: '迅雷影天堂', link: 'https://www.xl720.com/?s=' + unititle, selector: `h3 a[title*='${unititle}']` },
            { name: '迅影网', link: 'http://www.xunyingwang.com/search?q=' + unititle, selector: 'div.row p.movie-name' },
            // { name: '阳光电影', link: 'http://s.ygdy8.com/plus/so.php?kwtype=0&searchtype=title&keyword=' + gunititle, selector: "div.co_area2 table[border='0'][width='100%']" },
            { name: '扬天影视', link: 'https://www.mcyt.cn/?s=' + unititle, selector: 'div.mainleft div.info' },
            { name: '一只大榴莲', link: 'http://www.llduang.com/?s=' + unititle, selector: 'div.mainleft div.info' },
            { name: '音范丝', link: 'http://www.yinfans.com/?s=' + unititle, selector: `div.thumbnail a[title*='${unititle}']` },
            { name: '影海', link: 'http://www.yinghub.com/search/list.html?keyword=' + unititle, selector: 'div.row div.info' },
            { name: '影视看看', link: 'http://www.yskk.tv/index.php?m=vod-search&wd=' + unititle, selector: 'div.movielist li' },
            { name: '云播网', link: 'http://www.yunbowang.cn/index.php?m=vod-search&wd=' + unititle, selector: 'div.container div.col-xs-7' },
            { name: '中国高清网', link: 'http://gaoqing.la/?s=' + unititle, selector: 'div.mainleft div.thumbnail' },
            // { name: '宅腐资源站', link: 'http://www.zhaifu.cc/plus/search.php?kwtype=0&q=' + gunititle, selector: 'div.content a.focus' },
            { name: '宅客', link: 'https://www.zhaiiker.com/?post_type=post&s=' + unititle + ' 下载', selector: '#main h2.entry-title' },
            { name: '最新影视站', link: 'http://www.zxysz.com/?s=' + unititle, selector: '#content li.p-item' },
        ]
    });

    site_map.push({
        name: "BT国内网站",
        label: [
            { name: 'BT@烧包', link: 'http://www.btsbao.com/search-' + unititle + '.htm', selector: 'div.row div.media-body' },
            { name: 'BT吧', link: 'http://www.btba.cc/search?keyword=' + unititle, selector: 'div.left li' },
            { name: 'BT部落', link: 'http://www.btbuluo.com/s/' + unititle + '.html', selector: `h2 a:contains(${unititle})` },
            { name: 'BT下吧', link: 'http://www.btxiaba.com/index.php?m=vod-search&wd=' + unititle, selector: '#content p.pl' },
            { name: 'BT之家', link: 'http://www.btbtt.me/search-index-keyword-' + unititle + '.htm', selector: '#threadlist table' },
            // { name: '不太灵', method: "post", link: 'http://bt0.com/e/search/', data: `keyboard=${gongwang}&show=title%2Cbtname%2Cimdb%2Cdouban_id%2Cmvtitle&tbname=torrent&tempid=3&orderby=onclick`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: "div.row div.col-sm-3" },
            { name: '查片源', link: 'https://www.chapianyuan.com/?keyword=' + unititle, selector: 'div.block li' },
            { name: '磁力猫', link: 'http://www.cilimao.me/search?word=' + unititle, selector: '#Search__content_left___2MajJ div.MovieCard__content___3kv1W' },   // TODO check
            { name: '磁力站', link: 'http://oabt004.com/index/index?c=&k=' + unititle, selector: 'div.link-list-wrapper ul.link-list' },
            { name: '飞客BT', link: 'http://feikebt.com/s/' + unititle + '.html', selector: 'div.ppwrapper div.categorybar' },
            { name: '小浣熊下载', link: `https://www.xiaohx.org/search?key=${unititle}`, selector: `div.result_p a[title*='${unititle}']` },
            { name: '一站搜', link: 'http://v.yizhansou.com/mv/search?kw=' + unititle, selector: 'table > tbody > tr:nth-child(2)' },
            { name: '榆木林', link: 'http://www.yumuli.com/cili/s/' + unititle, selector: `h2.search-title a[title*='${unititle}']` },
        ]
    });

    site_map.push({
            name: "影视网盘搜索",
            label: [
                { name: '56网盘影', link: 'http://www.56wangpan.com/search/o2kw' + unititle, selector: `div.title > a[title*='${unititle}']` },
                { name: 'Kikibt影', method: "post", link: 'http://kikibt.cc/', data: `keyword=${unititle}`, headers: { "Content-Type": "application/x-www-form-urlencoded" }, rewrite_href: true, selector: 'div.list-area dl.item' },
                { name: 'NCCKL影', link: 'https://so.ncckl.cn/?page=1&name=' + unititle, ajax: 'https://www.yunpanjingling.com/search/' + unititle + '?sort=size.desc', selector: 'div.search-list div.name' },
                { name: '盘多多影视', link: 'http://www.panduoduo.net/s/comb/n-' + unititle + '&f-f4', selector: `h3 > a[title*='${unititle}']` },
                { name: '小白盘影视', link: 'http://www.xiaobaipan.com/list-' + unititle + '.html?order=size', selector: 'h4.job-title a' },
                { name: '云盘精灵影', link: 'https://www.yunpanjingling.com/search/' + unititle + '?sort=size.desc', selector: 'div.search-list div.name' },
                // { name: '茶杯狐', method: "post", type: "json", link: 'https://www.cupfox.com/?type=video&key=' + unititle, ajax: "https://www.cupfox.com/search", data: `search_type=video&key=${unititle}`, csrf: { name: "_xsrf", update: "data" },headers: {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, selector: 'title.length > 0' },
            ]
        });

     // 执行的主函数
    function site_exist_status() {
        $("#drdm_req_status").show();
        for (let i = 0; i < site_map.length; i++) {
            let map_dic = site_map[i];
            // if (GM_getValue(delete_site_prefix + map_dic.name, false)) {
            //     continue;
            // }
            $('#adv-sites').append(`<div class="c-aside name-offline" data-id="${i}"><h4><i>${map_dic.name}</i>· · · · · ·</h4><div class=c-aside-body style="padding: 0 12px;"> <ul class="bs" > </ul> </div> </div>`);

            let in_site_html = $(`div[data-id='${i}'] ul.bs`);
            for (let j = 0; j < map_dic.label.length; j++) {
                let label = map_dic.label[j];
            //     if (GM_getValue(delete_site_prefix + label.name, false)) {
            //         continue;
            //     }
                in_site_html.append(`<a href="${label.link}" data-name="${label.name}" target="_blank" rel="nofollow" class="name-offline">${label.name}</a>`);
                // if (GM_getValue("enable_adv_auto_search", true)) {
                //     Exist_check(label);
                // }
            }
        }

        update_status_interval = window.setInterval(update_req_status, 1e3);

        // if (!GM_getValue("enable_adv_auto_search", true)) {
        //     $("#drdm_req_status_hide").click();
        // }
    }
    site_exist_status();

});





