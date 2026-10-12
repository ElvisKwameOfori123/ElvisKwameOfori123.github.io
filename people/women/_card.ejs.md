```{=html}
<div class="people-grid list">
<% for (const item of items) { %>
  <article class="person-card" data-topic="<%- item.filter %>" <%= metadataAttrs(item) %>>
    <a href="<%- item.href %>" class="person-card-link" aria-label="Read profile of <%- item.name %>">
      <div class="person-image-wrap">
        <div class="person-image-pending" aria-hidden="true">
          <span class="person-initials"><%- item.name.substring(0, 1) %></span>
          <span class="person-image-note">Research profile</span>
        </div>
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