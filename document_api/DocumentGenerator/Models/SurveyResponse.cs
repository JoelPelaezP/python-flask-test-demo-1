namespace DocumentGenerator.Models
{
    using System;
    using System.ComponentModel.DataAnnotations;

    public class SurveyResponse
    {
        public SurveyResponse()
        {
            this.Location = string.Empty;
        }
        public required string Location { get; set; }
    }
}