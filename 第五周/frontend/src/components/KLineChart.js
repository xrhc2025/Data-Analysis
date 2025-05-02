import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const KLineChart = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/k_line');
      const data = await response.json();
      setChartData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    const chart = echarts.init(document.getElementById('k-line-chart'));
    const option = {
      tooltip: { trigger: 'axis' },
      xAxis: { data: chartData.map(item => item.name) },
      yAxis: {},
      series: [{
        type: 'candlestick',
        data: chartData.map(item => item.value)
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='k-line-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default KLineChart;