namespace DocumentGenerator.Models
{
    using System;
    using System.ComponentModel.DataAnnotations;

    public class Survey
    {
        [Required]
        public required string Name { get; set; }

        [Required]
        public required string LastName { get; set; }
    }
}