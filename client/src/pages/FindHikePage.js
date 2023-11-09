import React from "react";

import Header from "../layout/Header";
import HorizontalFilter from "../layout/HorizontalFilter";
import FindHike from "../components/FindHike";

function FindHikePage() {


  return (
    <div>
        <Header />
        <HorizontalFilter />
        <FindHike />
    </div>
  );
}

export default FindHikePage;
