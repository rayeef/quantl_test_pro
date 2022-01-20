const SHOW_LINE_CHART = document.querySelector('#showLineChart');
const SHOW_CANDLE_STICK_CHART = document.querySelector('#showCandleStickChart');


const createCSCElement = function(id){
  const stylesCSC = ["chart", "chart--axis-x--nowrap", "chart--points-invisible", "position-relative", "mh-15_6", "safari-overflow-hidden", "pt-4", "pt-md-5", "pb-1"];
  const CSC_ELEMENT = document.createElement('div');
  CSC_ELEMENT.id = id;
  CSC_ELEMENT.classList.add(...stylesCSC);
  CSC_ELEMENT.setAttribute("ref", "cscRef")
  return CSC_ELEMENT;
}

const addCSCElement = function(element, container){
  container.appendChild(element);
}

const removeCSCElement = function(elementId, container){
  const eleCSC = document.querySelector(`#${elementId}`);
  if(eleCSC !== null){
    container.removeChild(eleCSC);
  }
}

//CSC -> Candle Stick Chart
//LC -> Line Chart
const SPY_CSC_CONTAINER = document.querySelector("#SPY");
const SPY_LC_ELEMENT = document.querySelector('#lineChartSPY');

const QQQ_CSC_CONTAINER = document.querySelector("#QQQ");
const QQQ_LC_ELEMENT = document.querySelector('#lineChartQQQ');

const BTC_CSC_CONTAINER = document.querySelector("#bitcoin");
const BTC_LC_ELEMENT = document.querySelector('#lineChartBTC');

const ETH_CSC_CONTAINER = document.querySelector("#ethereum");
const ETH_LC_ELEMENT = document.querySelector('#lineChartETH');


const cscEleTabs = {
  "SPY-tab" : "candleStickChartSPY",
  "QQQ-tab" : "candleStickChartQQQ",
  "bitcoin-tab" : "candleStickChartBTC",
  "ethereum-tab" : "candleStickChartETH",
};

const cscEleContainerTabs = {
  "SPY-tab" : SPY_CSC_CONTAINER,
  "QQQ-tab" : QQQ_CSC_CONTAINER,
  "bitcoin-tab" : BTC_CSC_CONTAINER,
  "ethereum-tab" : ETH_CSC_CONTAINER,
};

const lcEleWRTTabs = {
  "SPY-tab" : SPY_LC_ELEMENT,
  "QQQ-tab" : QQQ_LC_ELEMENT,
  "bitcoin-tab" : BTC_LC_ELEMENT,
  "ethereum-tab" : ETH_LC_ELEMENT,
};

//data from apis

const dataSPY = JSON.parse(document.getElementById('spy_list').textContent);
const dataQQQ = JSON.parse(document.getElementById('qqq_list').textContent);
const dataBTC = JSON.parse(document.getElementById('btc_list').textContent);
const dataETH = JSON.parse(document.getElementById('eth_list').textContent);

// Will take html element & data as input
function createCandleStickChart(HtmlEle, data){

  const chart = LightweightCharts.createChart(HtmlEle, {
    width: 930,
    height: 320,
    layout: {
      backgroundColor: "#ffffff",
      textColor: "#868e96"
    },
    grid: {
      vertLines: {
        color: "rgba(197, 203, 206, 0.5)",
        visible: false,
      },
      horzLines: {
        color: "rgba(197, 203, 206, 0.5)",
        visible: false,
      }
    },
    crosshair: {
      mode: LightweightCharts.CrosshairMode.Normal
    },
    leftPriceScale: {
      borderColor: "#868e96"
    },
    timeScale: {
      borderColor: "#868e96"
    }
  });
  chart.applyOptions({
    priceScale: {
        position: 'left',
    },
    timeScale:{
      fixLeftEdge: true,
    },
  });
  new ResizeObserver(entries => { 
    if (entries.length === 0 || entries[0].target !== HtmlEle) { return; } 
    const newRect = entries[0].contentRect; 
    chart.applyOptions({ height: newRect.height, width: newRect.width }); }).observe(HtmlEle);

  
  const candlestickSeries = chart.addCandlestickSeries({
    upColor: "#3AB795",
    downColor: "#FF3860",
    borderVisible: false,
    wickVisible: true,
    borderUpColor: "#3AB795",
    borderDownColor: "#FF3860",
    wickUpColor: "#3AB795",
    wickDownColor: "#FF3860"
  });
  candlestickSeries.setData(data);
}

function setCSCCharts(selectedTabId = "SPY-tab", LC_ELEMENT, CSCData){
   
  //Create Element
  const CSC_ELEMENT = createCSCElement(cscEleTabs[selectedTabId]);
  //Add Chart
  createCandleStickChart(CSC_ELEMENT, CSCData);
  CSC_ELEMENT.style.display = "none";


  //Add to container
  addCSCElement(CSC_ELEMENT, cscEleContainerTabs[selectedTabId])
  //As by default Line Chart is selected
  SHOW_LINE_CHART.parentElement.classList.add('active');
  SHOW_CANDLE_STICK_CHART.parentElement.classList.remove('active');

  SHOW_CANDLE_STICK_CHART.onclick = function () {
    const liClassList = Array.from(SHOW_CANDLE_STICK_CHART.parentElement.classList);
    if(!liClassList.includes('active')){
      SHOW_CANDLE_STICK_CHART.parentElement.classList.add('active');
      SHOW_LINE_CHART.parentElement.classList.remove('active');
      LC_ELEMENT.style.display = "none";
      CSC_ELEMENT.style.display = "block";
    }
    //For preventing refreshing on <a> tag
    return false;
  }

  SHOW_LINE_CHART.onclick = function () {
    const liClassList = Array.from(SHOW_LINE_CHART.parentElement.classList);
    if(!liClassList.includes('active')){
      SHOW_LINE_CHART.parentElement.classList.add('active');
      SHOW_CANDLE_STICK_CHART.parentElement.classList.remove('active');
      CSC_ELEMENT.style.display = "none";
      LC_ELEMENT.style.display = "block";
    }
    //For preventing refreshing on <a> tag
    return false;
  }
}

//As the initial tab is SPY TAB
setCSCCharts('SPY-tab', SPY_LC_ELEMENT, dataSPY);

//tab elements
$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
  removeCSCElement(cscEleTabs[e.relatedTarget.id], cscEleContainerTabs[e.relatedTarget.id]);
  if(e.target.id === 'SPY-tab'){
    lcEleWRTTabs[e.relatedTarget.id].style.display = "block";
    setCSCCharts('SPY-tab', SPY_LC_ELEMENT, dataSPY);
  } else if(e.target.id === 'QQQ-tab'){
    lcEleWRTTabs[e.relatedTarget.id].style.display = "block";
    setCSCCharts('QQQ-tab', QQQ_LC_ELEMENT, dataQQQ);
  } else if(e.target.id === 'bitcoin-tab'){
    lcEleWRTTabs[e.relatedTarget.id].style.display = "block";
    setCSCCharts('bitcoin-tab', BTC_LC_ELEMENT, dataBTC);
  } else if(e.target.id === 'ethereum-tab'){
    lcEleWRTTabs[e.relatedTarget.id].style.display = "block";
    setCSCCharts('ethereum-tab', ETH_LC_ELEMENT, dataETH);
  } else{
    console.log(`No event registered for ${e.target} element`);
  }
});