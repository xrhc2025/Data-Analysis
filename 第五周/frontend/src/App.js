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

  const fetchData = async (type) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_chart_data/${type}`);
      const data = await response.json();
      setChartData(data || []);
      setChartType(type);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  useEffect(() => {
    fetchData('pie');
  }, []);

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
  }, [chartType, chartData]);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['pie']}>
          <Menu.Item key="pie" onClick={() => fetchData('pie')}>饼图</Menu.Item>
          <Menu.Item key="bar" onClick={() => fetchData('bar')}>柱状图</Menu.Item>
          <Menu.Item key="line" onClick={() => fetchData('line')}>折线图</Menu.Item>
          <Menu.Item key="graph" onClick={() => fetchData('graph')}>关系图谱</Menu.Item>
          <Menu.Item key="scatter" onClick={() => fetchData('scatter')}>散点图</Menu.Item>
          <Menu.Item key="radar" onClick={() => fetchData('radar')}>雷达图</Menu.Item>
          <Menu.Item key="path" onClick={() => fetchData('path')}>路径图</Menu.Item>
          <Menu.Item key="k_line" onClick={() => fetchData('k_line')}>K线图</Menu.Item>
          <Menu.Item key="tree" onClick={() => fetchData('tree')}>树图</Menu.Item>
          <Menu.Item key="treemap" onClick={() => fetchData('treemap')}>矩形树图</Menu.Item>
          <Menu.Item key="sunburst" onClick={() => fetchData('sunburst')}>旭日图</Menu.Item>
          <Menu.Item key="sankey" onClick={() => fetchData('sankey')}>桑基图</Menu.Item>
          <Menu.Item key="funnel" onClick={() => fetchData('funnel')}>漏斗图</Menu.Item>
          <Menu.Item key="pictorial_bar" onClick={() => fetchData('pictorial_bar')}>象形柱图</Menu.Item>
        </Menu>
      </Sider>
      <Layout style={{background: '#f0f2f5'}}>
        <Content style={{ margin: '16px' }}>
          {chartType === 'k_line' && <KLineChart />}
          {chartType === 'tree' && <TreeChart />}
          {chartType === 'treemap' && <Treemap />}
          {chartType === 'sunburst' && <SunburstChart />}
          {chartType === 'sankey' && <SankeyChart />}
          {chartType === 'funnel' && <FunnelChart />}
          {chartType === 'pictorial_bar' && <PictorialBarChart />}
          <div id="chart" style={{ width: '100%', height: '80vh' }}></div>
        </Content>
      </Layout>
    </Layout>
  );
}

export default App;
