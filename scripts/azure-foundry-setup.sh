#!/usr/bin/env bash
set -euo pipefail

# User email (included everywhere it's needed)
# Override with environment variable if needed: USER_EMAIL=your@email.com ./azure-foundry-setup.sh
USER_EMAIL="${USER_EMAIL:-donniechen92@gmail.com}"

# 0. Ensure Azure CLI is installed and you are signed in
echo "Step 0: Sign in interactively if not already signed in..."
az account show >/dev/null 2>&1 || az login

# 1. List subscriptions for this account and let user choose if multiple
echo "Finding subscriptions for $USER_EMAIL..."
mapfile -t SUB_IDS < <(az account list --all --query "[?user.name=='$USER_EMAIL'].{name:name,id:id}" -o tsv | awk '{print $2}')
mapfile -t SUB_NAMES < <(az account list --all --query "[?user.name=='$USER_EMAIL'].{name:name,id:id}" -o tsv | awk '{print $1}')

if [ ${#SUB_IDS[@]} -eq 0 ]; then
  echo "No subscriptions found for $USER_EMAIL. Confirm you're signed in with that account."
  exit 1
elif [ ${#SUB_IDS[@]} -eq 1 ]; then
  SUBSCRIPTION_ID="${SUB_IDS[0]}"
  echo "Using subscription: ${SUB_NAMES[0]} (${SUBSCRIPTION_ID})"
else
  echo "Multiple subscriptions found for $USER_EMAIL. Choose one by number:"
  for i in "${!SUB_IDS[@]}"; do
    idx=$((i+1))
    printf "%2d) %s  %s\n" "$idx" "${SUB_NAMES[i]}" "${SUB_IDS[i]}"
  done
  read -rp "Enter number of subscription to use: " choice
  if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#SUB_IDS[@]}" ]; then
    echo "Invalid choice."
    exit 1
  fi
  sel=$((choice-1))
  SUBSCRIPTION_ID="${SUB_IDS[$sel]}"
  echo "Selected subscription: ${SUB_NAMES[$sel]} (${SUBSCRIPTION_ID})"
fi

# 2. Set the active subscription
az account set --subscription "$SUBSCRIPTION_ID"
echo "Active subscription set to $SUBSCRIPTION_ID"

# 3. Create resource group (Australia East) with tags
RG_NAME="${RG_NAME:-foundry-rg-donnie}"
LOCATION="${LOCATION:-australiaeast}"
echo "Creating resource group $RG_NAME in $LOCATION..."
az group create \
  --name "$RG_NAME" \
  --location "$LOCATION" \
  --tags Project="Foundry-Basic" Owner="$USER_EMAIL" \
  --output none
echo "Resource group created or already exists."

# 4. Create the Foundry (AIServices) resource in Basic mode
FOUNDRY_NAME="${FOUNDRY_NAME:-foundry-donnie-92-8f3b1c}"  # ensure this is globally unique; change if needed
echo "Creating Cognitive Services AIServices account $FOUNDRY_NAME..."
az cognitiveservices account create \
  --name "$FOUNDRY_NAME" \
  --resource-group "$RG_NAME" \
  --kind AIServices \
  --sku S0 \
  --location "$LOCATION" \
  --allow-project-management \
  --output none

# 5. Wait for provisioning to succeed (polling)
echo "Waiting for provisioning to complete (this may take a few minutes)..."
MAX_RETRIES=60  # Maximum 10 minutes (60 * 10 seconds)
RETRY_COUNT=0
while true; do
  state=$(az cognitiveservices account show --name "$FOUNDRY_NAME" --resource-group "$RG_NAME" --query "properties.provisioningState" -o tsv)
  echo "Provisioning state: $state"
  if [ "$state" = "Succeeded" ]; then
    break
  fi
  if [ "$state" = "Failed" ]; then
    echo "Provisioning failed. Check the Azure portal for details."
    exit 1
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Timeout: Provisioning did not complete within the expected time. Check the Azure portal for status."
    exit 1
  fi
  sleep 10
done

# 6. Show endpoint and keys
echo "Foundry resource details:"
az cognitiveservices account show \
  --name "$FOUNDRY_NAME" \
  --resource-group "$RG_NAME" \
  --query "{name:name, location:location, sku:sku.name, endpoint:properties.endpoint}" \
  --output table

echo ""
echo "WARNING: The following command will display sensitive access keys."
echo "Keep these keys secure and do not share them publicly."
echo ""
echo "Listing keys (use these in SDK or portal if needed):"
az cognitiveservices account keys list \
  --name "$FOUNDRY_NAME" \
  --resource-group "$RG_NAME" \
  --output table

# 7. Assign Azure AI Owner role to your email at the resource group scope
SCOPE="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RG_NAME"
echo "Assigning role 'Azure AI Owner' to $USER_EMAIL at scope $SCOPE..."
if az role assignment create \
  --assignee "$USER_EMAIL" \
  --role "Azure AI Owner" \
  --scope "$SCOPE" \
  --output none; then
  echo "Role assignment successful."
else
  echo "WARNING: Role assignment failed. You may not have permission to create role assignments."
  echo "This is optional but recommended for managing the resource. Contact your admin if needed."
fi

# 8. Print portal URL
echo ""
echo "Portal URL (open in browser):"
echo "https://portal.azure.com/#resource/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RG_NAME/providers/Microsoft.CognitiveServices/accounts/$FOUNDRY_NAME/overview"

echo "Done."
