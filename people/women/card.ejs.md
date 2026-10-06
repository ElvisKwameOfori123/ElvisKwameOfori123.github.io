```{=html}
<div class="people-grid list">
<% for (const item of items) { 
  const initials = (item.name || "")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("");
%>
  <article class="person-card" data-topic="<%- item.filter %>" <%= metadataAttrs(item) %>>
    <a href="<%- item.path %>" class="person-card-link" aria-label="Read profile of <%- item.name %>">
      <div class="person-image-wrap">
        <% if (item.image) { %>
          <img src="<%- item.image %>" alt="<%- item['image-alt'] || ('Portrait of ' + item.name) %>" loading="lazy">
        <% } else { %>
          <div class="person-image-pending" role="img" aria-label="Portrait clearance pending for <%- item.name %>">
            <span class="person-initials"><%- initials %></span>
            <span class="person-image-note">Portrait clearance pending</span>
          </div>
        <% } %>
      </div>
      <div class="person-card-body">
        <h2 class="listing-name person-name"><%- item.name %></h2>
        <p class="listing-field person-field"><%- item.field %></p>
        <p class="listing-question person-question"><%- item.question %></p>
      </div>
    </a>
  </article>
<% } %>
</div>
```