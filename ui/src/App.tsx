import React, {ReactElement, useState} from 'react';
import { Button, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import axios from 'axios'

interface AnalysisData {
  isAnalysing: boolean;
  totalToAnalyse: number;
  alreadyAnalysed: number;
  message: string;
}

const App = (): ReactElement => {

  let polling: any = undefined;

  const [analysisData, setAnalysisData] = useState<AnalysisData>({
    isAnalysing: false,
    message: "",
    totalToAnalyse: 0,
    alreadyAnalysed: 0
  });

  const pollAnalysisStatus = async () => {
    const apiUrl = "http://127.0.0.1:5000/get-result";
    const response: any = await axios.get(apiUrl);

    if (response.data.status === "DONE") {
      clearInterval(polling);
      setAnalysisData({
        ...analysisData,
        isAnalysing: false,
        message: response.data.message
      })
    } else {
      setAnalysisData({
        isAnalysing: true,
        totalToAnalyse: parseInt(response.data.total_to_analyse),
        alreadyAnalysed: parseInt(response.data.analysed),
        message: response.data.message
      })
    }
  }

  const triggerAnalysis = async (): Promise<any> => {
    const apiUrl = "http://127.0.0.1:5000/start-analysis";
    try {
      const reponse = await axios.get(apiUrl);

      // start polling
      polling = setInterval(() => pollAnalysisStatus(), 1000);

    } catch(err) {
      console.error(err);
    }
  }

  const button = (disabled: boolean) => {

    let button = (
      <div>
        {disabled ? (
          <Button type="button" variant="primary" disabled onClick={triggerAnalysis}>
              Analyze media files
          </Button>
        ): 
          <Button type="button" variant="primary" onClick={triggerAnalysis}>
              Analyze media files
          </Button>
        }
      </div>
    )

    return button;
  }

  const loadingSpinner = (nrOfTotal: number, nrOfDone: number) => {
    return (
      <div>
        <Spinner animation="border" variant="primary"></Spinner>
        <h5>{nrOfDone} of {nrOfTotal}</h5> 
      </div>
      
    )
  }

  let disabled;
  if (analysisData.isAnalysing) {
    disabled = true;
  } else {
    disabled = false;
  }

  return (
    <div>
      <div>Status: {analysisData.message}</div>
      {
        button(disabled)
      }
      {
        analysisData.isAnalysing ? 
        loadingSpinner(analysisData.totalToAnalyse, analysisData.alreadyAnalysed)
        :
        ""
      }
    </div>
  )
}

export default App;
