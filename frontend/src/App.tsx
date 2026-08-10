import {
  Routes,
  Route
} from "react-router-dom";
import ExamSummary from "./pages/ExamSummary";
import TakeExam from "./pages/TakeExam";
import Result from "./pages/Result";
import UploadPDF from "./pages/UploadPDF";

function App() {

  return (

    <Routes>

  <Route
    path="/"
    element={<UploadPDF />}
  />

  <Route
    path="/exam/:id"
    element={<ExamSummary />}
  />

  <Route
    path="/attempt/:id"
    element={<TakeExam />}
  />
  <Route
    path="/result"
    element={<Result />}
  />

</Routes>

  );

}

export default App;