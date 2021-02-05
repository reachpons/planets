$repoimagename = $args[0]
#$repoimagename="alcolizerrepouat"
if ($null -eq $repoimagename)
{
Write-Host "Enter the value for the repoimagename parameter"
}
else
{
Write-Host "------------1: You are logging into "(Get-STSCallerIdentity).Arn
$account_id = (Get-STSCallerIdentity).Account
$commd1= "(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin "+$account_id+".dkr.ecr.ap-southeast-2.amazonaws.com"
Invoke-Expression $commd1

Write-Host "------------2: Starting to Build Docker container"
$commd2= "docker build -t $repoimagename ."
Invoke-Expression $commd2

Write-Host "------------3: Build successfully completed"
$commd3="docker tag "+$repoimagename+":latest "+$account_id+".dkr.ecr.ap-southeast-2.amazonaws.com/"+$repoimagename+":latest"
Invoke-Expression $commd3

Write-Host "------------4: Container Tagged with latest"
$commd4 ="docker push "+$account_id+".dkr.ecr.ap-southeast-2.amazonaws.com/"+$repoimagename+":latest"
Invoke-Expression $commd4
Write-Host "------------5: Container pushed into AWS ECR"
}