## Auto-Finances

- I can set transaction alerts on my credit cards to my email address
- I can access my emails using the Gmail API (a Python or JS client wrapping the Gmail API would work too)
- I can use Gmail query strings to find the transaction alerts with the following labels: INBOX & UNREAD & following from line: "chase" "discover"
- I can loop through matching messages to:
  - extract the neccessary data
  - write the data to a CSV
  - remove the INBOX & UNREAD labels
  - add the appropriate Auto-Finances labels
- if it's completely scripted I can migrate it to a Raspberry pi in my own house
- I can back-up my data to S3
  - I can back-up my data and make it accessible for viewing by working with the Google Sheets API (or just build a front-end)
