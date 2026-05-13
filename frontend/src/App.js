import React, { useState } from "react";

function App() {

  const [command, setCommand] = useState("");

  const [workflow, setWorkflow] = useState([]);

  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(false);


  const generateWorkflow = () => {
    if (!command.trim()) {

      alert("Please enter a command");

      return;
    }

    const generatedWorkflow = [

      {
        step: 1,
        component: "email_reader"
      },

      {
        step: 2,
        component: "llm_extractor"
      },

      {
        step: 3,
        component: "validator"
      },

      {
        step: 4,
        component: "api_caller"
      }

    ];

    setWorkflow(generatedWorkflow);
  };


  const runWorkflow = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/run-workflow",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            workflow: [

              {
                step: 1,
                component: "pdf_parser",
                params: {
                  pdf_path: "day3/sample3.pdf"
                }
              },

              {
                step: 2,
                component: "llm_extractor",
                params: {}
              },

              {
                step: 3,
                component: "validator",
                params: {}
              }

            ]
          })
        }
      );

      const data = await response.json();

      setLogs(data.execution_log);

    } catch (error) {

      console.log(error);

    }

    setLoading(false);
  };


  return (

    <div style={{ padding: "30px", fontFamily: "Arial" }}>

      <h1>AI Workflow Builder</h1>


      {/* VIEW 1 */}

      <div style={{ marginBottom: "30px" }}>

        <h2>1. Command Input</h2>

        <input
          type="text"
          placeholder="Type command..."
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          style={{
            padding: "10px",
            width: "300px"
          }}
        />

        <button
          onClick={generateWorkflow}
          style={{
            marginLeft: "10px",
            padding: "10px"
          }}
        >
          Generate Workflow
        </button>

      </div>


      {/* VIEW 2 */}

      <div style={{ marginBottom: "30px" }}>

        <h2>2. Workflow Canvas</h2>

        <div style={{ display: "flex", gap: "20px" }}>

          {workflow.map((node) => (

            <div
              key={node.step}
              style={{
                border: "1px solid black",
                padding: "20px",
                borderRadius: "10px",
                minWidth: "120px",
                textAlign: "center"
              }}
            >

              <h3>Step {node.step}</h3>

              <p>{node.component}</p>

            </div>

          ))}

        </div>

      </div>


      {/* VIEW 3 */}

      <div>

        <h2>3. Execution Status</h2>

        <button
          onClick={runWorkflow}
          style={{
            padding: "10px"
          }}
        >
          Run Workflow
        </button>

        {loading && <p>Running workflow...</p>}

        <div style={{ marginTop: "20px" }}>

          {logs.map((log, index) => (

            <div
              key={index}
              style={{
                border: "1px solid gray",
                marginBottom: "10px",
                padding: "10px",
                borderRadius: "10px"
              }}
            >

              <h4>{log.component}</h4>

              <pre>
                {JSON.stringify(log.result, null, 2)}
              </pre>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default App;