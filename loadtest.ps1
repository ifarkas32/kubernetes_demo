param(
    [int]$Workers = 100,
    [int]$Duration = 60,
    [string]$Url = 'http://localhost:30081/api/names'
)

python "$PSScriptRoot\loadtest\loadtest.py" --workers $Workers --duration $Duration --url $Url
