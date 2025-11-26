### **Hackathon Documented Guidelines**

**Overview:** Teams must create an innovative Agentic AI solution for dynamic pricing. While the scenario is a "Ride Share Company," the solution must demonstrate reasoning applicable to Honeywell’s catalog demand, supply constraints, and customer tiers.

**Timeline:**

* **Planning:** November 20 – November 30\. Collecting ideas, resources, setting up database, adjustments to your data set, everything but the functional code can be done ahead of time.  
* **Development:** December 1 – December 4\. Building all functional application code, think the code nextjs frontend and langchain backend, n8n workflows, connecting mcp servers & utilization.  
* **Judging & Presentations:** December 5\. Panel from Honeywell, ASU & Revature.

**Submission Protocol:**

* **Pre-presentation:** All written documentation, diagrams, and demo videos must be submitted via your GitHub repo prior to the judging sessions on Dec 5 to mitigate connectivity issues.

**Deliverables (Presentation \- 15 Mins Total):**

* **Audience:** Your panel consists of stakeholders with **varying degrees of technical expertise** (e.g., Business Executives vs. Technical Architects).  
  1. **Strategy:** Keep your main presentation clear, concise, and accessible. Do not lose the non-technical audience by "diving into the weeds" of code.Audience members seeking a better technical understanding can always ask quesitons.  
* **Depth:** Focus on the *business value* and the *logic flow* during the demo. Reserve complex technical implementation details for the Q\&A session, where experts may probe deeper.  
* **Format:** 10 min presentation, 5 min Q\&A.  
  1. **UX Demo (Primary Focus):** A live visualization demonstrating the AI-generated pricing strategy and goodness measures within the interface.  
  2. **Short Deck:**  
     1. **Architecture:** A diagram demonstrating how the Agentic app collects information & reasons.  
     2. **Honeywell Bridge:** Recommendations on how this Ride Share solution applies to Honeywell’s dynamic pricing.

**Scrum Approach:** Treat the trainers as active Scrum Masters. Validate your approach early to trim requirements if the scope feels too large.

 

### **"Sparks" \- Ideas for scoping the problem statement**

*Select a specific problem area to focus your Agent's reasoning. Your Agent should consider ONE NOT ALL of the following. Feel free to also come up with your own idea and pitch it to the trainers. NOTE: Not all of these elements are contained within dataset to give you ideas of how you might need to expand the dataset (mock this expansion):*

* **Targeting Profitability:** We need to find a way to maximize single-rider profitability during high-traffic hours without losing the customer based on elements such as Competitor Rates, Historical Route Cost, and Booking Lead Time.  
* **Handling Scarcity:** We need to find a way to dynamically adjust pricing during regional supply shortages based on elements such as Driver Supply, Demand Intensity, and Time of Day.  
* **Loyalty Logic:** We need to find a way to apply 'surge protection' logic for high-value relationships based on elements such as Loyalty Tier, Annual Business Volume, and Contract Obligations.  
* **Asset Quality:** We need to find a way to scale price points based on asset hierarchy (e.g., Luxury vs. Standard)" based on elements such as Vehicle Type, Asset Condition, and Pricing Integrity Rules.

Instructions  
\-Attached is the presentation from Honeywell, as well as the dataset regarding ridesharing. Feel free to expand on the simple dataset to make your data more robust to fit the needs of your solution.

Consider the rows in the data as their own unique customer booking:  
 

| Column Name | Description |
| :---- | :---- |
| **Number\_of\_Riders** | Represents the **demand** level. This is the number of riders (or ride requests) in the vicinity at the time of booking. High numbers indicate high demand. |
| **Number\_of\_Drivers** | Represents the **supply** level. This is the number of drivers available in the vicinity at the time of booking. Low numbers indicate low supply. |
| **Location\_Category** | The classification of the location where the ride was booked. |
| **Customer\_Loyalty\_Status** | The loyalty tier of the customer booking the ride. |
| **Number\_of\_Past\_Rides** | The total number of rides this specific customer has taken in the past. |
| **Average\_Ratings** | The average rating associated with the customer (or arguably the driver/service in that context), often used as a quality or trust metric. |
| **Time\_of\_Booking** | The time of day the booking was made. |
| **Vehicle\_Type** | The class of vehicle requested for the ride. |
| **Expected\_Ride\_Duration** | The estimated time the ride will take to complete |
| **Historical\_Cost\_of\_Ride** | The actual cost of the ride recorded historically. This is typically the **target variable** you are trying to predict or optimize. |

 

References  
 [HON dynamic pricing hackathon](https://app-ms.revature.com/apigateway/kernel/unsecure/artifactsdownload/files/batchCurriculum/9415/0)  
 [hackathon\_dataset](https://app-ms.revature.com/apigateway/kernel/unsecure/artifactsdownload/files/batchCurriculum/9416/0)  
