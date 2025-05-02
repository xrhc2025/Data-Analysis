import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import "./App.css";

function App() {
  const [input1, setInput1] = useState("");
  const [input2, setInput2] = useState("");
  const [input3, setInput3] = useState("");
  const [response, setResponse] = useState("");

  const handleGet = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/get?${new URLSearchParams({
          param: input1,
        })}`
      );
      const data = await res.json();
      setResponse(data.message);
    } catch (err) {
      setResponse("请求失败: " + err.message);
    }
  };

  const handlePost = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/post?param=${input3}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ body_param: input2 }),
        }
      );
      const data = await res.json();
      setResponse(`${data.body_param}, ${data.query_param}`);
    } catch (err) {
      setResponse("请求失败: " + err.message);
    }
  };
  return (
    <div className="App">
      <h1>前后端联调示例</h1>
      {/* 请求输入框区域 */}
      <div>
        <div className="input-box">
          <input
            type="text"
            value={input1}
            onChange={(e) => setInput1(e.target.value)}
            placeholder="GET请求参数"
          />
          <button onClick={handleGet}>发送GET请求</button>
        </div>
        <div className="input-box">
          <div className="post-box">
            <input
              type="text"
              value={input2}
              onChange={(e) => setInput2(e.target.value)}
              placeholder="POST请求body参数"
            />
            <input
              type="text"
              value={input3}
              onChange={(e) => setInput3(e.target.value)}
              placeholder="POST请求query参数"
            />
          </div>
          <button onClick={handlePost}>发送POST请求</button>
        </div>
      </div>
      {/* 响应结果区域 */}
      <div className="response-box">
        <h3>响应结果：</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

