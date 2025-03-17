To build a Contact Sync Service to Microsoft 365 for Hitobito, follow the steps outlined below:

### Step 1: Identify Existing Contact Sync Services
1. **Review Existing Implementations in Hitobito**
   - There are existing contact synchronization services in the Hitobito repository, such as the Mailchimp synchronization. Refer to these services for implementation patterns and design principles.

   Example: `spec/domain/synchronize/mailchimp/synchronizator_spec.rb`

### Step 2: Explore Microsoft 365 Integration
1. **Understand Microsoft 365 Contacts API**
   - Familiarize yourself with the Microsoft 365 Contacts API. Key resources include:
     - [Outlook personal contacts API overview](https://learn.microsoft.com/en-us/graph/outlook-contacts-concept-overview)
     - [Microsoft Graph Outlook API for mail, calendars, and contacts](https://learn.microsoft.com/en-us/exchange/client-developer/exchange-web-services/office-365-rest-apis-for-mail-calendars-and-contacts)
     - [Get Started with the Outlook REST APIs](https://learn.microsoft.com/en-us/outlook/rest/get-started)
  
### Follow-Up Steps
1. **Define a Clear Plan**
   - Based on the findings, create a detailed plan for building the Contact Sync Service, including data flow, authentication, and error handling.

2. **Create a Prototype**
   - Develop a prototype utilizing identified libraries or by creating new modules.
   - Ensure to integrate the necessary authentication mechanisms with Microsoft 365 (e.g., OAuth 2.0).

### Implementation Example
Here is a simplified example of how you might start integrating the Microsoft 365 Contacts API with Hitobito:

```ruby
# app/services/microsoft365_contact_sync_service.rb

require 'net/http'
require 'json'

class Microsoft365ContactSyncService
  MICROSOFT_GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"

  def initialize(access_token)
    @access_token = access_token
  end

  def sync_contacts(hitobito_contacts)
    hitobito_contacts.each do |contact|
      create_or_update_contact(contact)
    end
  end

  private

  def create_or_update_contact(contact)
    uri = URI("#{MICROSOFT_GRAPH_API_BASE_URL}/me/contacts")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true

    request = Net::HTTP::Post.new(uri.path, headers)
    request.body = contact_data(contact).to_json

    response = http.request(request)
    handle_response(response)
  end

  def headers
    {
      "Authorization" => "Bearer #{@access_token}",
      "Content-Type" => "application/json"
    }
  end

  def contact_data(contact)
    {
      "givenName" => contact.first_name,
      "surname" => contact.last_name,
      "emailAddresses" => [
        {
          "address" => contact.email,
          "name" => "#{contact.first_name} #{contact.last_name}"
        }
      ],
      "businessPhones" => [contact.phone_number]
    }
  end

  def handle_response(response)
    case response
    when Net::HTTPSuccess
      puts "Contact synced successfully"
    else
      puts "Error syncing contact: #{response.body}"
    end
  end
end
```

### Resources for Further Reading
- [Microsoft Graph Documentation](https://learn.microsoft.com/en-us/graph/)
- [Office 365 REST APIs for Mail, Calendars, and Contacts](https://learn.microsoft.com/en-us/exchange/client-developer/exchange-web-services/office-365-rest-apis-for-mail-calendars-and-contacts)

For additional details, you can view more results directly in the [Hitobito repository](https://github.com/hitobito/hitobito).
