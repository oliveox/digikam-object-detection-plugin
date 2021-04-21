## TODO
- logging to file and console
- start analysis API    
    - loading bar - incremental update
    - bidirectional communication using websockets
- support for multiple Digikam root albums
- ML efficiency analysis: export somewhere the pics but with border around  detected objects
- restart Digikam after object analysis
- create db class models
- run it externally 
- reconnect UI afte refresh to to server status

## DONE
- stop polling after analysis done
- create config file (removed hardcoded vars)
- unique constraints in internal db
- print stacktrace
- close digikam connecitons after using them
- skip entities that were already analysed
- put inside ImageObjects unsupported files too
- shut up the tensorflow init logs

- if analysis is already running, don't retrigger it at a new api call 
        - ignore any other api calls
        - disable trigger button
- button to trigger the analysis
- analysis process status polling