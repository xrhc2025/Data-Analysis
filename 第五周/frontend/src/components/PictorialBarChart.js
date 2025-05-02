import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const PictorialBarChart = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/pictorial_bar');
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
    const chart = echarts.init(document.getElementById('pictorial-bar-chart'));
    const option = {
      tooltip: { trigger: 'axis' },
      xAxis: { data: chartData.map(item => item.name) },
      yAxis: {},
      series: [{
        type: 'pictorialBar',
        data: chartData.map(item => item.value),
        symbol: 'roundRect',
        symbolSize: ['120%', '100%'],
        symbolOffset: [0, 0],
        symbolRepeat: true,
        symbolMargin: '1%'
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='pictorial-bar-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default PictorialBarChart;