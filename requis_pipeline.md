
# function `execute_phase_1`
## Params: 
- Enum embeding model
- enum ML model
- Path to monolith src code

## Returns 
JSON
```
{
  "applicationClasses": [
    {
      "className": “x”,
      "className": “x”
    }
  ]
}
```

# fonction `execute_phase_2` 
## Params: 
- JSON returned from execute_phase_1
- Enum phase 2 model

## Returns
JSON 

```
{
  "applicationServices": {
    "service": [
      {
        "className": "x"
      },
      {
        "className": "x"
      }
    ],
    “service: [
      {
        "className": "x"
      },
      {
        "className": "x"
      }
    ]
  },
  "utilityServices": {
    "service": [
      {
        "className": "x"
      },
      {
        "className": "x"
      }
    ]
  },
  "entityServices": {
    "service": [
      {
        "className": "x"
      },
      {
        "className": "x"
      }
    ]
  }
}
```

# Function `execute_phase_3` 
## Params: 
- JSON returned from execute_phase_2
- Enum model phase 3

## Returns
JSON 

```
{
  "microservices": {
    "microservice": {
      "applicationServices": {
        "service": [
          {
            "className": "x"
          },
          {
            "className": "x"
          }
        ],
        "service": [
          {
            "className": "x"
          },
          {
            "className": "x"
          }
        ]
      },
      "utilityServices": {
        "service": [
          {
            "className": "x"
          },
          {
            "className": "x"
          }
        ]
      },
      "entityServices": {
        "service": [
          {
            "className": "x"
          },
          {
            "className": "x"
          }
        ]
      }
    }
  }
}
```
