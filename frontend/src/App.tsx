import {
  Routes,
  Route
} from "react-router-dom";
import ExamDashboard from "./pages/ExamDashboard";
import TakeExam from "./pages/TakeExam";
import Result from "./pages/Result";
import UploadPDF from "./pages/UploadPDF";
//import ExamDashboard from "./pages/ExamDashboard";

function App() {

  return (

    <Routes>

  <Route
    path="/"
    element={<UploadPDF />}
  />

  <Route
    path="/exam/:id"
    element={<ExamDashboard />}
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