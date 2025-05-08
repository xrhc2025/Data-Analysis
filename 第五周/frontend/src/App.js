import React, { useState, useEffect } from 'react';
  import { Layout, Menu } from 'antd';
 // 修改导入语句以适配 ECharts
  import * as echarts from 'echarts';
import './App.css';
import KLineChart from './components/KLineChart';
import TreeChart from './components/TreeChart';
import Treemap from './components/Treemap';
import SunburstChart from './components/SunburstChart';
import SankeyChart from './components/SankeyChart';
import FunnelChart from './components/FunnelChart';
import PictorialBarChart from './components/PictorialBarChart';

const { Content, Sider } = Layout;

function App() {
  const [chartType, setChartType] = useState('');
  const [chartData, setChartData] = useState([]);
  // 查询到的所有数据
  const [targetData, setTargetData] = useState([]);

  const fetchData = async (type) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_chart_data/${type}`);
      // const response = await fetch(`http://82.156.195.106:7001/get_chart_data/${type}`);
      const data = await response.json();
      // setChartData(data || []);
      setTargetData(data || []);
      setChartType(type);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  useEffect(() => {
    fetchData('pie');
  }, []);
  useEffect(() => {
    // 类型变化时处理数据
    if (chartType) {
      // 假设你有一个函数来处理数据
      const processedData = processData(targetData);
      setChartData(processedData);
    }
  }, [chartType]);
const processData = (data) => {
  if (!data || !data.length) return [];
  
  switch (chartType) {
    case 'pie':
    case 'bar':
    case 'line':
    case 'scatter':
    case 'radar':
    case 'path':
    case 'funnel':
    case 'pictorial_bar':
      return data.map(item => ({
        name: item.title,
        value: item.rating
      }));
    
    case 'graph':
      const nodes = data.map(item => ({
        id: item.title,
        name: item.title,
        symbolSize: item.rating * 2,
        category: item.genres.split(' ')[0]
      }));
      
      const links = [];
      for (let i = 0; i < nodes.length - 1; i++) {
        links.push({
          source: nodes[i].id,
          target: nodes[i + 1].id
        });
      }
      
      return { nodes, links };
    
    case 'china_map':
      return data.filter(item => item.countries === '中国').map(item => ({
        name: item.title,
        value: item.rating
      }));
    
    default:
      return data;
  }
};

  useEffect(() => {
    const chart = echarts.init(document.getElementById('chart'));
    let option;
    switch (chartType) {
      case 'pie':
        option = {
          tooltip: { trigger: 'item' },
          series: [{
            type: 'pie',
            data: chartData
          }]
        };
        break;
      case 'bar':
        option = {
          tooltip: { trigger: 'axis' },
          xAxis: { data: chartData.map(item => item.name) },
          yAxis: {},
          series: [{
            type: 'bar',
            data: chartData.map(item => item.value)
          }]
        };
        break;
      case 'line':
        option = {
          tooltip: { trigger: 'axis' },
          xAxis: { data: chartData.map(item => item.name) },
          yAxis: {},
          series: [{
            type: 'line',
            data: chartData.map(item => item.value)
          }]
        };
        break;
      case 'china_map':
        echarts.registerMap('china', {type: 'FeatureCollection', features: chartData.features});
        option = {
          tooltip: { trigger: 'item' },
          series: [{
            type: 'map',
            map: 'china',
            data: chartData
          }]
        };
        break;
      case 'graph':
        option = {
          tooltip: {},
          series: [{
            type: 'graph',
            layout: 'force',
            force: { repulsion: 1000 },
            data: chartData.nodes,
            links: chartData.links
          }]
        };
        break;
      case 'scatter':
        option = {
          tooltip: { trigger: 'item' },
          xAxis: {},
          yAxis: {},
          series: [{
            type: 'scatter',
            data: chartData
          }]
        };
        break;
      case 'radar':
        option = {
          tooltip: { trigger: 'item' },
          radar: {
            indicator: [
              { name: 'A', max: 100 },
              { name: 'B', max: 100 },
              { name: 'C', max: 100 },
              { name: 'D', max: 100 },
              { name: 'E', max: 100 }
            ]
          },
          series: [{
            type: 'radar',
            data: chartData
          }]
        };
        break;
      case 'path':
        option = {
          tooltip: { trigger: 'axis' },
          xAxis: {},
          yAxis: {},
          series: [{
            type: 'line',
            data: chartData,
            symbol: 'circle',
            symbolSize: 10
          }]
        };
        break;
      default:
        break;
    }
    if (option) {
      chart.setOption(option);
    }
    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['pie']}>
          <Menu.Item key="pie" onClick={() => setChartType('pie')}>饼图</Menu.Item>
          <Menu.Item key="bar" onClick={() => setChartType('bar')}>柱状图</Menu.Item>
          <Menu.Item key="line" onClick={() => setChartType('line')}>折线图</Menu.Item>
          <Menu.Item key="graph" onClick={() => setChartType('graph')}>关系图谱</Menu.Item>
          <Menu.Item key="scatter" onClick={() => setChartType('scatter')}>散点图</Menu.Item>
          <Menu.Item key="radar" onClick={() => setChartType('radar')}>雷达图</Menu.Item>
          <Menu.Item key="path" onClick={() => setChartType('path')}>路径图</Menu.Item>
          {/*<Menu.Item key="k_line" onClick={() => setChartType('k_line')}>K线图</Menu.Item>
          <Menu.Item key="tree" onClick={() => setChartType('tree')}>树图</Menu.Item>
          <Menu.Item key="treemap" onClick={() => setChartType('treemap')}>矩形树图</Menu.Item>
          <Menu.Item key="sunburst" onClick={() => setChartType('sunburst')}>旭日图</Menu.Item>
          <Menu.Item key="sankey" onClick={() => setChartType('sankey')}>桑基图</Menu.Item>
          <Menu.Item key="funnel" onClick={() => setChartType('funnel')}>漏斗图</Menu.Item>
          <Menu.Item key="pictorial_bar" onClick={() => setChartType('pictorial_bar')}>象形柱图</Menu.Item>*/}
        </Menu>
      </Sider>
      <Layout style={{background: '#f0f2f5'}}>
        <Content style={{ margin: '16px' }}>
          {/*{chartType === 'k_line' && <KLineChart />}
          {chartType === 'tree' && <TreeChart />}
          {chartType === 'treemap' && <Treemap />}
          {chartType === 'sunburst' && <SunburstChart />}
          {chartType === 'sankey' && <SankeyChart />}
          {chartType === 'funnel' && <FunnelChart />}
          {chartType === 'pictorial_bar' && <PictorialBarChart />}*/}
          <div id="chart" style={{ width: '100%', height: '80vh' }}></div>
        </Content>
      </Layout>
    </Layout>
  );
}

export default App;
