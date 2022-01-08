import React, { useState } from "react";

function useDataFetching(asyncCallback) {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState({});

  useEffect(async () => {}, []);
}

export default useDataFetching;
