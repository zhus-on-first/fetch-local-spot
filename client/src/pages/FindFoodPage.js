import React from "react";

import Header from "../layout/Header";
import HorizontalFilter from "../layout/HorizontalFilter";
import FindFood from "../components/FindFood";

function FindFoodPage() {


  return (
    <div>
        <Header />
        <HorizontalFilter />
        <FindFood />
    </div>
  );
}

export default FindFoodPage;
