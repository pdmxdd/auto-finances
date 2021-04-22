## MVP

A python script that when run will:

1. get gmail account label names and label ids
2. find all the messages matching the following gmail query strings:
  - from:"chase" label:INBOX label:UNREAD subject:"Your Single Transaction Alert from Chase
  - from:"discover" label:INBOX label:UNREAD subject:"Transaction Alert"
3. loop through the messages and: 
  1. extract the following information:
    - gmail_message_id
    - gmail_thread_id
    - Date
    - From
    - To
    - Subject
    - condensed_message
    - vendor
    - amount
    - authorized_time
  2. write the information to a local CSV file
  3. from the message remove the following labels:
    - INBOX
    - UNREAD
  4. add the Auto-Finances/Recorded label to the message
  5. add the Auto-Finances/Chase or Auto-Finances/Discover label to the message