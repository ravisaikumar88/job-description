import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");
  const [copied, setCopied] = useState(false);

  const handleExtract = async () => {
    if (!url) {
      setResult("Please enter a valid job link.");
      return;
    }

    setResult("Processing...");

    try {
      // Use environment variable or fallback to production backend URL
      const apiUrl = import.meta.env.VITE_API_URL || "https://job-description-1wnm.onrender.com";
      const response = await fetch(`${apiUrl}/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Server error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.status === "error") {
        setResult(`Error: ${data.message || "Failed to extract job details"}`);
      } else {
        setResult(data.formatted_message || "Error generating message.");
      }
    } catch (error) {
      console.error("Extraction error:", error);
      setResult(`Backend error: ${error.message || "Make sure the server is running."}`);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);

    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#1a1a1a",
        color: "white",
        padding: "20px",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "600px",
          padding: "20px",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            marginBottom: "30px",
            fontSize: "32px",
            fontWeight: "bold",
          }}
        >
          Job Auto Formatter
        </h1>

        {/* Input Box */}
        <input
          type="text"
          placeholder="Paste job link here..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            width: "100%",
            padding: "14px",
            marginBottom: "15px",
            borderRadius: "8px",
            fontSize: "16px",
            border: "1px solid #555",
            background: "#2a2a2a",
            color: "white",
          }}
        />

        {/* Button */}
        <button
          onClick={handleExtract}
          style={{
            width: "100%",
            padding: "14px",
            fontSize: "16px",
            cursor: "pointer",
            borderRadius: "8px",
            border: "none",
            background: "#000",
            color: "white",
            marginBottom: "20px",
            fontWeight: "bold"
          }}
        >
          Generate Job Post
        </button>

        {/* Output Box */}
        <div
            style={{
              background: "#f7f7f7",
              color: "black",
              padding: "18px",
              borderRadius: "10px",
              minHeight: "100px",
              fontSize: "15px",
              lineHeight: "1.5",
              whiteSpace: "pre-wrap",
            }}
            dangerouslySetInnerHTML={{
              __html: result
                .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // bold
                .replace(/\n/g, "<br/>") // newlines
            }}
          ></div>

        {/* Copy Button */}
        {result && result !== "Processing..." && (
          <>
            <button
              onClick={copyToClipboard}
              style={{
                marginTop: "12px",
                padding: "12px 20px",
                fontSize: "16px",
                cursor: "pointer",
                width: "100%",
                borderRadius: "8px",
                border: "none",
                fontWeight: "bold",
                background: "#333",
                color: "white",
              }}
            >
              Copy Message
            </button>

            {copied && (
              <p
                style={{
                  color: "lightgreen",
                  marginTop: "10px",
                  textAlign: "center",
                }}
              >
                Copied!
              </p>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
