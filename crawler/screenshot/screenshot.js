const puppeteer = require('puppeteer');

const urls = [
	"https://opengov.seoul.go.kr/mediahub/11089478",
	"https://www.byedust.net/02",
	"http://kfem.or.kr/?p=187396",
	"https://www.bbc.com/korean/news-43524873",
	"http://mnews.jtbc.joins.com/News/Article.aspx?news_id=NB11609490",
	"http://www.monews.co.kr/news/articleView.html?idxno=114666",
	"http://jkjtv.kr/%EC%84%9C%EC%9A%B8%EC%8B%9C%EC%9D%98-%EC%9D%B4%EC%83%81%ED%95%9C-%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80-%EB%8C%80%EC%B1%85%EB%B0%95%EC%84%9D%EC%88%9C-%EA%B5%90%EC%88%98%EC%9D%98-%EC%A7%84%EC%A7%9C/",
	"http://techm.kr/bbs/board.php?bo_table=article&wr_id=3967",
	"http://www.medipana.com/news/news_viewer.asp?NewsNum=220098&MainKind=A&NewsKind=5&vCount=12&vKind=1",
	"books.google.co.kr/books?id=qYU0DwAAQBAJ&pg=PT33&lpg=PT33&dq=미세먼지+대비책&source=bl&ots=6M3O0u2OKd&sig=tDsh4-vufMLWOgZMxLNB7VVEtZk&hl=ko",
	"https://news.joins.com/article/21860676",
	"http://biz.chosun.com/site/data/html_dir/2017/08/18/2017081801505.html",
	"https://www.huffingtonpost.kr/2017/08/21/story_n_17794862.html",
	"http://www.hankookilbo.com/v/65436643715042099ec59b0384c5e835",
	"http://www.sisapress.com/journal/article/170925",
	"http://www.gnmaeil.com/news/articleView.html?idxno=350144",
	"http://www.sisajournal-e.com/biz/article/187111",
	"http://v.media.daum.net/v/20170816141016383",
	"http://www.hitnews.co.kr/news/articleList.html?page=7&total=565&sc_section_code=S1N1&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm",
	"http://wpalss.tistory.com/tag",
	"https://banksalad.com/contents/가상화폐-개념-완벽-정리-A-to-Z-1부-WYTtp",
	"https://steemit.com/kr/@kim066/4urqt9-part-1",
	"http://bryan.wiki/167",
	"http://www.mobiinside.com/kr/2017/03/20/blockchain_1-2/",
	"http://imnews.imbc.com/replay/2018/nwdesk/article/4501645_22663.html",
	"https://ggclip.com/video/3uRNaxfK_1s/%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8-part-2-%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8%EC%9D%98-%EC%9B%90%EB%A6%AC-feat-%ED%95%B4%EC%8B%9C-4%EC%B0%A8%EC%82%B0%EC%97%85%ED%98%81%EB%AA%85%E3%85%A3%EB%B6%81%EC%8A%A4%ED%86%A0%EB%9E%91-book'staurant.html",
	"http://www.kinews.net/news/articleView.html?idxno=71193",
	"http://samsung.dkyobobook.co.kr/Kyobo_T3/Content/ebook/ebook_View.asp?barcode=4808957821220&product_cd=001&category_id=021303",
	"http://news.donga.com/3/all/20010727/7719949/1",
	"http://www.cryptocoin.kr/entry/%EB%A7%88%EC%9D%B4%EB%8B%9D%ED%92%80-%ED%97%88%EB%B8%8C-%EB%A9%80%ED%8B%B0%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%B1%84%EA%B5%B4%EC%84%A4%EC%A0%95-9%EB%8B%A8%EA%B3%84-Ethash-Equihash",
	"https://twitter.com/hashtag/방탄소년단컴백",
	"http://www.yonhapnews.co.kr/bulletin/2018/04/17/0200000000AKR20180417028000005.HTML",
	"https://www.huffingtonpost.kr/entry/bts-new-album_kr_5afe5782e4b0463cdba03f6d",
	"http://www.nocutnews.co.kr/news/4974463",
	"http://www.nocutnews.co.kr/news/4955614",
	"http://www.vlive.tv/video/81944/%EC%B2%AB-%EA%B9%9C%EC%A7%9D-%EB%9D%BC%EC%9D%B4%EB%B8%8C%E2%99%A1-%EB%A6%AC%EC%96%BC%EB%A6%AC%ED%8B%B0-%EB%B3%B4%EC%85%A8%EB%82%98%EC%9A%94",
	"http://www.sportsseoul.com/news/read/662538",
	"https://lemurtube.com/results?search_query=%23%EB%B0%A9%ED%83%84%EC%86%8C%EB%85%84%EB%8B%A8%EC%BB%B4%EB%B0%B1%EC%87%BC",
	"http://bender-gd.de/1032wwj/jffzoo2.php?fbnaccxif=highlight-eng-sub",
	"http://m.fnnews.com/news/201807271247530338",
	"http://m.blog.naver.com/fnxmdl334/220927075942",
	"https://www.huffingtonpost.kr/2014/10/05/story_n_5934218.html",
	"https://www.clien.net/service/board/use/7337559",
	"http://massukr.tistory.com/81",
	"http://research-paper.co.kr/news/view/47433",
	"https://videos.tube/video/acIeWlZZ5bk/-30-",
	"https://nhacchobe.net/video/L3iJXBwnc9Y/1-mi-one-vape-review.html",
	"http://www.monews.co.kr/news/articleView.html?idxno=105479",
	"http://www.newsen.com/news_view.php?uid=201108301430354100",
	"http://www.newswire.co.kr/newsRead.php?no=567071",
	"https://www.tripadvisor.co.kr/Attractions-g298085-Activities-Da_Nang_Quang_Nam_Province.html",
	"https://www.skyscanner.co.kr/news/places-to-visit-in-danang",
	"https://triple.guide/regions/22b60e7e-afc7-40e1-9237-8f31ed8a842d/articles/6bb1f9e0-cfda-49af-a40b-7339b3a10ed6",
	"https://withvolo.com/trip/r3wvdlr2",
	"https://brunch.co.kr/@allstay/270",
	"https://www.hyatt.com/ko-KR/hotel/vietnam/hyatt-regency-danang-resort-and-spa/danhr",
	"http://previewdeal.wemakeprice.com/deal/adeal/2300639/991800/?source=991800&no=44",
	"https://www.wotif.com/Da-Nang-Hotels-Fivitel-Da-Nang.h20144297.Hotel-Information",
	"http://www.pictame.com/tag/%EB%8B%A4%EB%82%AD%EB%AA%85%EC%86%8C",
	"http://www.10puzzle.com/piece/5757-%EC%86%90%EC%98%A4%EA%B3%B5%EC%9D%B4-%EC%88%98%EB%A0%A8%ED%95%9C-%EB%8B%A4%EB%82%AD%EB%AA%85%EC%86%8C-%EB%A7%88%EB%B8%94%EB%A7%88%EC%9A%B4%ED%8B%B4-%EB%B0%A9%EB%B0%A9%EC%BD%95%EC%BD%95.html"
	];

(async () => {
	const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  for(let i=0;i<urls.length;i++) if([10, 14, 21, 22, 23, 29, 31, 37, 40, 43, 52, 53, 54, 58].includes(i)) {
  	let url = urls[i];
  	try{
	  	await page.goto(url, {waitUntil: 'networkidle2', timeout: 0});
	  	await page.screenshot({path: '[' + i + '].png', fullPage: true});
	  }catch(exception){continue;}
  }
  await browser.close();
})();