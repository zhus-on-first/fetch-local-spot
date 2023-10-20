import React from "react"
import { Link } from "react-router-dom"

function HorizontalFilter() {
    return (
        <div className="horizontal-filter">
            <Link to="/find-hike">Find a Hike</Link> |
            <Link to="/find-spot">Find a Food Spot</Link> |
            <Link to="/find-ride">Find a Ride</Link> |
            <Link to="/post-report">Post a Report</Link> |
            <Link to="/#add-location">Add a Location</Link> |
            <Link to="/locations/1">Location1 Details</Link> |
        </div>
    )
}

export default HorizontalFilter