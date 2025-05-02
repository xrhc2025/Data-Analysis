import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const SankeyChart = () => {
  const [chartData, setChartData] = useState({ nodes: [], links: [] });

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/sankey');
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
    const chart = echarts.init(document.getElementById('sankey-chart'));
    const option = {
      tooltip: { trigger: 'item', triggerOn: 'mousemove' },
      series: [{
        type: 'sankey',
        data: chartData.nodes,
        links: chartData.links,
        emphasis: {
          focus: 'adjacency'
        },
        lineStyle: {
          normal: {
            curveness: 0.5,
            color: 'source',
            opacity: 0.8
          }
        }
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='sankey-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default SankeyChart;